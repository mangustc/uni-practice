from api.UserAuth import router as user_router
from api.Product import router as product_router
from api.Category import router as category_router
from api.SubCategory import router as subcategory_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(user_router)
router.include_router(product_router)
router.include_router(category_router)
router.include_router(subcategory_router)