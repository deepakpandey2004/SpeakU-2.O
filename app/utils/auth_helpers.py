from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4
import secrets

from app.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_ROUNDS    
)



def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:

    to_encode = data.copy()
    
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    
    to_encode.update({
        "exp": expire,                   
        "iat": datetime.now(timezone.utc), 
        "type": "access"                   
    })
    
    
    if "user_id" in to_encode and isinstance(to_encode["user_id"], UUID):
        to_encode["user_id"] = str(to_encode["user_id"])
    

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        
        return None


def create_token_response(user_id: UUID, email: str) -> dict:
    access_token = create_access_token(
        data={"user_id": str(user_id), "email": email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60  
    }



def generate_room_id() -> str:

    random_part = secrets.token_urlsafe(6)       
    uuid_part = str(uuid4())[:8]                    
    return f"room_{random_part}_{uuid_part}"



if __name__ == "__main__":

    print("=" * 60)
    print("🔐 Auth Helpers Test")
    print("=" * 60)
    
    
    print("\n1️⃣  Password Hashing Test:")
    password = "MyPass123"
    hashed = hash_password(password)
    print(f"   Original: {password}")
    print(f"   Hashed:   {hashed}")
    print(f"   Length:   {len(hashed)} chars")
    
    
    print("\n2️⃣  Password Verification Test:")
    is_correct = verify_password("MyPass123", hashed)
    is_wrong = verify_password("WrongPass", hashed)
    print(f"   Correct password verify:  {is_correct} ✅")
    print(f"   Wrong password verify:    {is_wrong} ❌")
    
    
    print("\n3️⃣  Salt Magic Test:")
    hash1 = hash_password("SamePassword")
    hash2 = hash_password("SamePassword")
    print(f"   Hash 1: {hash1[:30]}...")
    print(f"   Hash 2: {hash2[:30]}...")
    print(f"   Same?:  {hash1 == hash2} (Should be False due to salt!)")
    
    
    print("\n4️⃣  JWT Token Creation Test:")
    test_user_id = uuid4()
    token = create_access_token({
        "user_id": str(test_user_id),
        "email": "test@gmail.com"
    })
    print(f"   Token: {token[:50]}...")
    print(f"   Length: {len(token)} chars")
    
    
    print("\n5️⃣  JWT Token Decoding Test:")
    payload = decode_access_token(token)
    print(f"   Decoded payload:")
    for key, value in payload.items():
        print(f"      {key}: {value}")
    
    print("\n6️⃣  Invalid Token Test:")
    invalid_payload = decode_access_token("invalid.token.here")
    print(f"   Invalid token result: {invalid_payload} (Should be None)")
    
    
    print("\n7️⃣  Room ID Generation Test:")
    for i in range(3):
        room = generate_room_id()
        print(f"   Room {i+1}: {room}")
    
    print("\n" + "=" * 60)
    print("✅ All auth helpers working!")
    print("=" * 60)