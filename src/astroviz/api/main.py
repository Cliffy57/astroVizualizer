"""Main FastAPI application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from astroviz.api.routes import asteroids, visualization


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan management."""
    # Startup
    print("🚀 AstroViz starting up...")
    yield
    # Shutdown
    print("🛑 AstroViz shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="AstroViz API",
        description="Professional asteroid data visualization platform",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(asteroids.router, prefix="/api/v1/asteroids", tags=["asteroids"])
    app.include_router(
        visualization.router, prefix="/api/v1/viz", tags=["visualization"]
    )

    @app.get("/")
    async def root() -> JSONResponse:
        """Root endpoint."""
        return JSONResponse(
            {"message": "Welcome to AstroViz API", "version": "0.1.0", "docs": "/docs"}
        )

    @app.get("/health")
    async def health() -> JSONResponse:
        """Health check endpoint."""
        return JSONResponse({"status": "healthy"})

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "astroviz.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )
