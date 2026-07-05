from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
import json
import asyncio

from app.extensions import get_db, redis_client
from app.models import User, CallSession
from app.utils.auth_helpers import decode_access_token, generate_room_id
from app.config import settings


router = APIRouter()


 
class ConnectionManager:
    

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"✅ User connected: {user_id}")
        print(f"   Active connections: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
     
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"❌ User disconnected: {user_id}")
            print(f"   Active connections: {len(self.active_connections)}")

    async def send_to_user(self, user_id: str, message: dict):
        
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
                return True
            except Exception as e:
                print(f"⚠️ Failed to send to {user_id}: {e}")
                self.disconnect(user_id)
                return False
        return False

    def is_connected(self, user_id: str) -> bool:
        
        return user_id in self.active_connections



manager = ConnectionManager()



def get_user_from_token(token: str, db: Session) -> User:
    
    payload = decode_access_token(token)
    if not payload:
        return None

    user_id = payload.get("user_id")
    if not user_id:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    return user



@router.websocket("/find")
async def find_match(
    websocket: WebSocket,
    token: str = Query(..., description="JWT token for authentication"),
    db: Session = Depends(get_db)
):
    

    
    user = get_user_from_token(token, db)

    if not user:
        await websocket.close(code=1008, reason="Invalid token")
        return

    if not user.is_active:
        await websocket.close(code=1008, reason="Account inactive")
        return

    
    if not user.native_lang or not user.learning_lang:
        await websocket.close(
            code=1008,
            reason="Please complete your profile (set languages)"
        )
        return

    user_id = str(user.id)

    
    await manager.connect(user_id, websocket)

    try:
        
        await manager.send_to_user(user_id, {
            "type": "connected",
            "user_id": user_id,
            "username": user.username,
            "message": "Searching for a match..."
        })

        

        match_key = f"waiting:{user.learning_lang}:{user.native_lang}"
        partner_id = redis_client.get(match_key)

        if partner_id:
            
            print(f"🎯 Match found! {user_id} ↔ {partner_id}")

            
            redis_client.delete(match_key)

           
            partner = db.query(User).filter(User.id == partner_id).first()

            if not partner:
                
                await add_to_waiting_pool(user, user_id)
                return

            
            room_id = generate_room_id()

            
            call_session = CallSession(
                caller_id=partner.id,      
                receiver_id=user.id,         
                room_id=room_id,
                caller_language=partner.native_lang,
                receiver_language=user.native_lang,
                status="active"
            )
            db.add(call_session)
            db.commit()
            db.refresh(call_session)

            
            match_message_for_user = {
                "type": "match_found",
                "room_id": room_id,
                "session_id": str(call_session.id),
                "partner": {
                    "id": str(partner.id),
                    "username": partner.username,
                    "native_lang": partner.native_lang,
                    "learning_lang": partner.learning_lang,
                    "avg_rating": partner.avg_rating,
                    "total_calls": partner.total_calls
                },
                "message": f"Matched with {partner.username}! Starting call..."
            }

            match_message_for_partner = {
                "type": "match_found",
                "room_id": room_id,
                "session_id": str(call_session.id),
                "partner": {
                    "id": str(user.id),
                    "username": user.username,
                    "native_lang": user.native_lang,
                    "learning_lang": user.learning_lang,
                    "avg_rating": user.avg_rating,
                    "total_calls": user.total_calls
                },
                "message": f"Matched with {user.username}! Starting call..."
            }

            
            await manager.send_to_user(user_id, match_message_for_user)

            
            partner_notified = await manager.send_to_user(
                partner_id,
                match_message_for_partner
            )

            if not partner_notified:
                print(f"⚠️ Partner {partner_id} not connected, but session created")

        else:
            
            await add_to_waiting_pool(user, user_id)

        
        while True:
            try:
                data = await websocket.receive_text()

                
                try:
                    message = json.loads(data)
                    msg_type = message.get("type")

                    if msg_type == "ping":
                        await manager.send_to_user(user_id, {"type": "pong"})
                    elif msg_type == "cancel":
                        # User wants to cancel search
                        own_pool_key = f"waiting:{user.native_lang}:{user.learning_lang}"
                        redis_client.delete(own_pool_key)
                        await manager.send_to_user(user_id, {
                            "type": "cancelled",
                            "message": "Match search cancelled"
                        })
                        break

                except json.JSONDecodeError:
                    pass

            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected normally")

    except Exception as e:
        print(f"❌ Error in matchmaking: {e}")

    finally:
        
        own_pool_key = f"waiting:{user.native_lang}:{user.learning_lang}"
        redis_client.delete(own_pool_key)

        
        manager.disconnect(user_id)



async def add_to_waiting_pool(user: User, user_id: str):
    
    own_pool_key = f"waiting:{user.native_lang}:{user.learning_lang}"

    
    redis_client.set(
        own_pool_key,
        user_id,
        ex=300  
    )

    print(f"📋 Added to waiting pool: {own_pool_key} = {user_id}")

    await manager.send_to_user(user_id, {
        "type": "waiting",
        "message": "Added to waiting pool. Waiting for match...",
        "expires_in": 300
    })



@router.get("/stats", summary="Get matchmaking statistics")
def get_match_stats():
    
    return {
        "active_connections": len(manager.active_connections),
        "connected_users": list(manager.active_connections.keys())
    }