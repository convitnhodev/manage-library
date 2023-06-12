from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.base_class import Base
from service.base import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_applications():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app 




app = start_applications()

@app.get('/')
def hello_api():
    return {"details": settings.DATABASE_URL}