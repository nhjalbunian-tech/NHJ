from fastapi import APIRouter

from app.api.routes import (
    ai_takeoffs,
    approvals,
    audit,
    auth,
    documents,
    pricing,
    procurement,
    projects,
    roles,
    takeoffs,
    users,
    verify,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(projects.router)
api_router.include_router(documents.router)
api_router.include_router(takeoffs.router)
api_router.include_router(ai_takeoffs.router)
api_router.include_router(verify.router)
api_router.include_router(pricing.router)
api_router.include_router(procurement.router)
api_router.include_router(approvals.router)
api_router.include_router(audit.router)
