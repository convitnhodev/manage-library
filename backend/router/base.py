from fastapi import APIRouter

from router import router_cards

api_router = APIRouter()

api_router.include_router(router_cards.router, prefix="/card")