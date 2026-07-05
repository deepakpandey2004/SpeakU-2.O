from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
   
    APP_NAME: str = "SpeakU"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    

    DATABASE_URL: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    

    REDIS_URL: str
    REDIS_TOKEN: str
    


    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    

    BCRYPT_ROUNDS: int = 12
    
    

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5500"
    
    

    STUN_SERVER: str = "stun:stun.l.google.com:19302"
    
    

    LINGOS_NEW_USER_BONUS: int = 10
    LINGOS_PER_CALL_COST: int = 1
    LINGOS_PER_CALL_REWARD: int = 5
    
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == "development"


settings = Settings()



if __name__ == "__main__":
    
    print("=" * 50)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 50)
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode:  {settings.DEBUG}")
    print(f"Server:      {settings.HOST}:{settings.PORT}")
    print(f"Database:    {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"Redis:       {settings.REDIS_URL}")
    print(f"JWT Algo:    {settings.JWT_ALGORITHM}")
    print(f"CORS:        {settings.cors_origins_list}")
    print("=" * 50)
    print("✅ All settings loaded successfully!")