from fastapi import APIRouter

from service import router_cards
from service import router_users
from service import router_login
from service import router_rules

api_router = APIRouter()

api_router.include_router(router_cards.router, prefix="/card")
api_router.include_router(router_users.router, prefix="/user")
api_router.include_router(router_login.router, prefix="/login")
api_router.include_router(router_rules.router, prefix="/rule")
