from fastapi import FastAPI

from app.core.config import settings
from app.routes import cars, health


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(cars.router)
    
    return app


app = create_app()
