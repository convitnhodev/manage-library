from fastapi import APIRouter

from router import router_cards
from router import router_users

api_router = APIRouter()

api_router.include_router(router_cards.router, prefix="/card")
api_router.include_router(router_users.router, prefix="/user")