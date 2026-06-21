from fastapi import APIRouter

from app.routes.apartments import router as apartments_router

router = APIRouter()

# Proper SaaS-style namespace
router.include_router(
    apartments_router,
    prefix="/apartments",
    tags=["apartments"]
)