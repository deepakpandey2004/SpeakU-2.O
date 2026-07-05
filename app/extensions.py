from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from typing import Generator
import requests
import logging

from app.config import settings


logger = logging.getLogger(__name__)


engine = create_engine(
    settings.DATABASE_URL,
    

    poolclass=QueuePool,
    pool_size=5,              
    max_overflow=10,        
    pool_pre_ping=True,       
    pool_recycle=3600,        
    

    echo=settings.DEBUG,
    
    # Future-proof settings
    future=True
)


SessionLocal = sessionmaker(
    autocommit=False,    
    autoflush=False,     
    bind=engine,       
    expire_on_commit=False  
)



Base = declarative_base()



def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db          
    except Exception as e:
        db.rollback()     
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()        


class UpstashRedis:
    
    def __init__(self):
        self.url = settings.REDIS_URL
        self.token = settings.REDIS_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }
    
    def _request(self, command: list):
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json=command,
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("result")
        except requests.exceptions.RequestException as e:
            logger.error(f"Redis error: {e}")
            return None
    
    def set(self, key: str, value: str, ex: int = None):
        command = ["SET", key, value]
        if ex:
            command.extend(["EX", str(ex)])
        return self._request(command)
    
    def get(self, key: str):
        return self._request(["GET", key])
    
    def delete(self, key: str):
        return self._request(["DEL", key])
    
    def exists(self, key: str) -> bool:
        result = self._request(["EXISTS", key])
        return result == 1
    
    def ping(self) -> bool:
        result = self._request(["PING"])
        return result == "PONG"


redis_client = UpstashRedis()



def check_database_connection() -> bool:
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def check_redis_connection() -> bool:
    try:
        if redis_client.ping():
            logger.info("✅ Redis connection successful")
            return True
        else:
            logger.error("❌ Redis ping failed")
            return False
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        return False



if __name__ == "__main__":
    print("=" * 50)
    print("🔌 Testing Connections...")
    print("=" * 50)
    
    
    print("\n📊 Database (PostgreSQL/Supabase):")
    if check_database_connection():
        print("   ✅ Connected successfully!")
    else:
        print("   ❌ Connection failed!")
    

    print("\n🔴 Redis (Upstash):")
    if check_redis_connection():
        print("   ✅ Connected successfully!")
        
    
        print("\n🧪 Quick Redis Test:")
        redis_client.set("test_key", "Hello SpeakU!", ex=60)
        value = redis_client.get("test_key")
        print(f"   Set 'test_key' = 'Hello SpeakU!'")
        print(f"   Got 'test_key' = '{value}'")
        redis_client.delete("test_key")
        print(f"   Deleted 'test_key'")
    else:
        print("   ❌ Connection failed!")
    
    print("\n" + "=" * 50)
    print("✅ Extension tests complete!")
    print("=" * 50)