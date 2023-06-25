from fastapi import APIRouter

from router import router_cards
from router import router_users
from router import router_login
from router import router_rules
from router import router_library_loan_form
from router import router_books

api_router = APIRouter()

api_router.include_router(router_cards.router, prefix="/card")
api_router.include_router(router_users.router, prefix="/user")
api_router.include_router(router_login.router, prefix="/login")
api_router.include_router(router_rules.router, prefix="/rule")
api_router.include_router(router_library_loan_form.router, prefix="/library-loan-form")
api_router.include_router(router_books.router, prefix="/books")