from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from app.config.settings import settings
from app.database.connection import connect_to_mongo, close_mongo_connection
from app.middleware.cors import setup_cors
from app.routes.api import router as api_router
from app.websocket.routes import router as ws_router
from app.utils.logger import setup_logging

# Setup logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    print("🚀 Sentinel-AURA Backend started")

    yield

    # Shutdown
    await close_mongo_connection()
    print("🛑 Sentinel-AURA Backend stopped")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(api_router, prefix="/api", tags=["API"])
app.include_router(ws_router, tags=["WebSocket"])

@app.get("/")
async def root():
    return {"message": "Sentinel-AURA Backend API", "version": settings.app_version}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )