from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .config import get_settings
from .database import engine, Base
from .api.routes import auth, users

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up Auth Microservice...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Auth Microservice...")


# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    description="JWT-based Authentication Microservice with RBAC",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.debug
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.api_v1_str}/auth",
    tags=["authentication"]
)

app.include_router(
    users.router,
    prefix=f"{settings.api_v1_str}/users",
    tags=["users"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Auth Microservice API",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "JWT Authentication",
            "User Registration & Login",
            "Token Refresh",
            "Role-based Access Control",
            "Password Security"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth-microservice"}
