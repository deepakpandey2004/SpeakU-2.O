import asyncio
import websockets
import json
import sys


async def connect_and_match(username: str, token: str):
    
    
    url = f"ws://localhost:8000/match/find?token={token}"
    
    print("=" * 60)
    print(f"🔌 [{username}] Connecting to: {url}")
    print("=" * 60)
    
    try:
        async with websockets.connect(url) as websocket:
            print(f"✅ [{username}] Connected!")
            
            
            while True:
                try:
                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=60.0  
                    )
                    
                    data = json.loads(message)
                    msg_type = data.get("type")
                    
                    print(f"\n📩 [{username}] Received: {msg_type}")
                    print(json.dumps(data, indent=2))
                    
                    
                    if msg_type == "connected":
                        print(f"💡 [{username}] Waiting for match...")
                    
                    elif msg_type == "waiting":
                        print(f"⏳ [{username}] In waiting pool...")
                    
                    elif msg_type == "match_found":
                        print(f"\n🎉 [{username}] MATCH FOUND! 🎉")
                        partner = data.get("partner", {})
                        print(f"   Partner: {partner.get('username')}")
                        print(f"   Languages: {partner.get('native_lang')} → {partner.get('learning_lang')}")
                        print(f"   Room ID: {data.get('room_id')}")
                        print(f"   Session ID: {data.get('session_id')}")
                        
                        
                        await asyncio.sleep(10)
                        break
                    
                    elif msg_type == "cancelled":
                        print(f"❌ [{username}] Search cancelled")
                        break
                
                except asyncio.TimeoutError:
                    print(f"⏰ [{username}] Timeout - no match in 60s")
                    break
                except websockets.exceptions.ConnectionClosed:
                    print(f"🔌 [{username}] Connection closed by server")
                    break
    
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ [{username}] WebSocket error: {e}")
    except Exception as e:
        print(f"❌ [{username}] Error: {e}")
    
    print(f"\n👋 [{username}] Disconnected\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_websocket.py <username> <token>")
        print("Example: python test_websocket.py alice eyJhbGc...")
        sys.exit(1)
    
    username = sys.argv[1]
    token = sys.argv[2]
    
    asyncio.run(connect_and_match(username, token))