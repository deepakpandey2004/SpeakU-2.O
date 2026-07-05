from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from sqlalchemy.orm import Session
from typing import Dict, List
import json

from app.extensions import get_db
from app.models import User, CallSession
from app.utils.auth_helpers import decode_access_token


router = APIRouter()

class RoomManager:
    
    def __init__(self):
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}
    
    async def join_room(self, room_id: str, user_id: str, websocket: WebSocket):

        await websocket.accept()
        
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        
        self.rooms[room_id][user_id] = websocket
        
        print(f"✅ User {user_id} joined room {room_id}")
        print(f"   Room size: {len(self.rooms[room_id])}/2")
        
        
        await self.notify_peer_joined(room_id, user_id)
    
    def leave_room(self, room_id: str, user_id: str):
        
        if room_id in self.rooms and user_id in self.rooms[room_id]:
            del self.rooms[room_id][user_id]
            
            print(f"❌ User {user_id} left room {room_id}")
            
            
            if len(self.rooms[room_id]) == 0:
                del self.rooms[room_id]
                print(f"🗑️  Room {room_id} deleted (empty)")
    
    async def send_to_peer(self, room_id: str, sender_id: str, message: dict):
        
        if room_id not in self.rooms:
            return False
        
        
        for user_id, websocket in self.rooms[room_id].items():
            if user_id != sender_id:
                try:
                    await websocket.send_json(message)
                    return True
                except Exception as e:
                    print(f"⚠️ Failed to send to peer: {e}")
                    return False
        
        return False
    
    async def notify_peer_joined(self, room_id: str, user_id: str):
        
        await self.send_to_peer(room_id, user_id, {
            "type": "peer-joined",
            "user_id": user_id,
            "message": "Peer joined the room"
        })
    
    async def notify_peer_left(self, room_id: str, user_id: str):
        
        await self.send_to_peer(room_id, user_id, {
            "type": "peer-left",
            "user_id": user_id,
            "message": "Peer left the room"
        })
    
    def get_room_size(self, room_id: str) -> int:
        
        return len(self.rooms.get(room_id, {}))


room_manager = RoomManager()


@router.websocket("/signal/{room_id}")
async def webrtc_signaling(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(..., description="JWT token"),
    db: Session = Depends(get_db)
):
    
    
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    user_id = payload.get("user_id")
    if not user_id:
        await websocket.close(code=1008, reason="Invalid token payload")
        return
    
    
    session = db.query(CallSession).filter(
        CallSession.room_id == room_id,
        CallSession.status == "active"
    ).first()
    
    if not session:
        await websocket.close(code=1008, reason="Call session not found")
        return
    
    
    if user_id not in [str(session.caller_id), str(session.receiver_id)]:
        await websocket.close(code=1008, reason="You are not part of this call")
        return
    
    
    current_size = room_manager.get_room_size(room_id)
    if current_size >= 2:
        await websocket.close(code=1008, reason="Room is full")
        return
    
    
    await room_manager.join_room(room_id, user_id, websocket)
    
    
    await websocket.send_json({
        "type": "room-joined",
        "room_id": room_id,
        "user_id": user_id,
        "peers_in_room": room_manager.get_room_size(room_id),
        "message": "Joined room. Ready for signaling."
    })
    
    try:
        
        while True:
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                msg_type = message.get("type")
                
                print(f"📩 [{user_id}] Sent: {msg_type}")
                
                
                if msg_type in ["offer", "answer", "ice-candidate"]:
                    # Add sender info
                    message["from_user_id"] = user_id
                    
                    
                    relayed = await room_manager.send_to_peer(
                        room_id,
                        user_id,
                        message
                    )
                    
                    if relayed:
                        print(f"   ✅ Relayed {msg_type} to peer")
                    else:
                        print(f"   ⚠️ No peer to relay to")
                        await websocket.send_json({
                            "type": "error",
                            "message": "No peer in room"
                        })
                
                
                elif msg_type == "end-call":
                    # Notify peer
                    await room_manager.send_to_peer(room_id, user_id, {
                        "type": "call-ended",
                        "message": "Peer ended the call"
                    })
                    
                    
                    session.end_call()
                    db.commit()
                    
                    print(f"📞 Call ended in room {room_id}")
                    break
                
                
                elif msg_type == "ping":
                    await websocket.send_json({"type": "pong"})
                
                else:
                    print(f"   ⚠️ Unknown message type: {msg_type}")
            
            except json.JSONDecodeError:
                print(f"   ❌ Invalid JSON received")
                continue
    
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected from signaling")
    
    except Exception as e:
        print(f"❌ Signaling error: {e}")
    
    finally:
        
        await room_manager.notify_peer_left(room_id, user_id)
        room_manager.leave_room(room_id, user_id)



@router.get("/rooms/stats", summary="Get active signaling rooms")
def get_signaling_stats():
    """
    Get current signaling rooms statistics
    Useful for monitoring active calls
    """
    return {
        "active_rooms": len(room_manager.rooms),
        "rooms": {
            room_id: {
                "size": len(users),
                "users": list(users.keys())
            }
            for room_id, users in room_manager.rooms.items()
        }
    }