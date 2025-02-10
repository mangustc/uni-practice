from api.userAuthFile import router as user_router
from api.productFile import router as product_router
from api.categoryFile import router as category_router
from api.subCategoryFile import router as subcategory_router
from api.articleFile import router as article_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(user_router)
router.include_router(product_router)
router.include_router(category_router)
router.include_router(subcategory_router)
router.include_router(article_router)
