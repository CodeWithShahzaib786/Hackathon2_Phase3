"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os

# Import cleanup function
from src.services.chat_service import cleanup_inactive_sessions


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Start background task for session cleanup
    cleanup_task = asyncio.create_task(periodic_cleanup())

    yield

    # Shutdown: Cancel background task
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


async def periodic_cleanup():
    """Periodically clean up inactive chat sessions."""
    while True:
        try:
            await asyncio.sleep(300)  # Run every 5 minutes
            cleaned = cleanup_inactive_sessions()
            if cleaned > 0:
                print(f"Cleaned up {cleaned} inactive chat sessions")
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in session cleanup: {e}")


# Create FastAPI application
app = FastAPI(
    title="Todo Backend API",
    description="Backend API for Todo Full-Stack Web Application (Phase II + Phase III AI Chat)",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Todo Backend API",
        "version": "1.0.0",
        "docs": "/docs",
    }


# Import and include routers
from src.api import auth, tasks, chat

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
