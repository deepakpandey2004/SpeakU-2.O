from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

from app.config import settings
from app.extensions import check_database_connection, check_redis_connection


logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📍 Environment: {settings.ENVIRONMENT}")
    logger.info("=" * 60)
    
    logger.info("📊 Checking database connection...")
    if not check_database_connection():
        logger.error("❌ Database connection failed!")
        raise Exception("Cannot start without database")
    
    logger.info("🔴 Checking Redis connection...")
    if not check_redis_connection():
        logger.warning("⚠️  Redis connection failed (will retry on use)")
    
    logger.info("✅ Application ready!")
    logger.info(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"🌐 Frontend: http://{settings.HOST}:{settings.PORT}/")
    
    yield  
    
    logger.info("👋 Shutting down application...")


def create_app() -> FastAPI:
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Language Exchange Platform with Real Voice Calls",
        docs_url="/docs",                
        redoc_url="/redoc",              
        lifespan=lifespan                 
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],             
        allow_headers=["*"],              
    )
    
   
    @app.get("/health", tags=["Root"])
    async def health_check():
        db_status = check_database_connection()
        redis_status = check_redis_connection()
        
        return {
            "status": "healthy" if (db_status and redis_status) else "degraded",
            "services": {
                "database": "up" if db_status else "down",
                "redis": "up" if redis_status else "down"
            }
        }
    
    @app.get("/api", tags=["Root"])
    async def api_info():
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs"
        }
    
    
    from app.api import auth
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    
    from app.api import profile
    app.include_router(profile.router, prefix="/profile", tags=["Profile"])

    from app.api import rating
    app.include_router(rating.router, prefix="/rating", tags=["Rating"])

    from app.api import call
    app.include_router(call.router, prefix="/call", tags=["Call"])

    from app.api import match
    app.include_router(match.router, prefix="/match", tags=["Matchmaking"])

    from app.api import signaling
    app.include_router(signaling.router, prefix="/signaling", tags=["WebRTC Signaling"])
    

    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
    
    if os.path.exists(frontend_dir):
        # Mount static files (css, js, assets)
        app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
        app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
        
        # Serve HTML pages
        @app.get("/", include_in_schema=False)
        async def serve_index():
            return FileResponse(os.path.join(frontend_dir, "index.html"))
        
        @app.get("/index.html", include_in_schema=False)
        async def serve_index_html():
            return FileResponse(os.path.join(frontend_dir, "index.html"))
        
        @app.get("/login.html", include_in_schema=False)
        async def serve_login():
            return FileResponse(os.path.join(frontend_dir, "login.html"))
        
        @app.get("/register.html", include_in_schema=False)
        async def serve_register():
            return FileResponse(os.path.join(frontend_dir, "register.html"))
        
        @app.get("/profile.html", include_in_schema=False)
        async def serve_profile():
            return FileResponse(os.path.join(frontend_dir, "profile.html"))
        
        @app.get("/match.html", include_in_schema=False)
        async def serve_match():
            return FileResponse(os.path.join(frontend_dir, "match.html"))
        
        @app.get("/call.html", include_in_schema=False)
        async def serve_call():
            return FileResponse(os.path.join(frontend_dir, "call.html"))
        
        @app.get("/home.html", include_in_schema=False)
        async def serve_home():
            return FileResponse(os.path.join(frontend_dir, "home.html"))
        
        logger.info(f"✅ Frontend mounted from: {frontend_dir}")
    else:
        logger.warning(f"⚠️  Frontend directory not found: {frontend_dir}")
    
    logger.info(f"✅ App created: {settings.APP_NAME} v{settings.APP_VERSION}")
    
    return app