from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Set
from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import api_v1_router


class ConnectionManager:
    """Manages active WebSocket connections for live workflow and telemetry updates."""
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send to WebSocket client: {e}")
                self.disconnect(connection)


ws_manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycles."""
    logger.info(f"Starting {settings.APP_NAME} in [{settings.APP_ENV}] mode on port {settings.PORT}...")
    logger.info(f"Neon Database status: {'CONFIGURED' if settings.is_database_configured else 'UNCONFIGURED (SAFE MODE)'}")
    logger.info(f"Cloudinary status: {'CONFIGURED' if settings.is_cloudinary_configured else 'UNCONFIGURED (SAFE MODE)'}")
    logger.info(f"LinkedIn API status: {'CONFIGURED' if settings.is_linkedin_configured else 'UNCONFIGURED (SAFE MODE)'}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME} cleanly...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous Multi-Agent Content & Publishing Platform for LinkedIn",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
origins = list(set([
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(api_v1_router)


@app.get("/")
async def root():
    """Root discovery endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "api_v1": "/api/v1/health"
    }


@app.websocket("/ws/live")
async def websocket_live_endpoint(websocket: WebSocket):
    """Real-time streaming for agent state, workflow progress, and notifications."""
    await ws_manager.connect(websocket)
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "CONNECTION_ESTABLISHED",
            "message": "Connected to LinkedIn AgentOS Live Stream",
            "active_connections": len(ws_manager.active_connections)
        })
        while True:
            data = await websocket.receive_text()
            # Handle client pings or queries
            await websocket.send_json({"type": "PONG", "payload": data})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.APP_DEBUG)
