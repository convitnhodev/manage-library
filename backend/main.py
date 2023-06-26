from fastapi import FastAPI
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from db.base_class import Base
from router.base import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_applications():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)

    # Configure CORS
    origins = ["http://localhost:5173"]  # Replace with the origin(s) of your frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    create_tables()
    include_router(app)
    return app 




app = start_applications()

@app.get('/')
def hello_api():
    return {"details": settings.DATABASE_URL}