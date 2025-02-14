from api.userAuthFile import router as user_router
from api.productFile import router as product_router
from api.categoryFile import router as category_router
from api.articleFile import router as article_router
from api.filterFile import router as filter_router
from api.sortFile import router as sorted_router
from api.delivery import router as delivery_router
from api.characteristicFile import router as characteristic_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(user_router)
router.include_router(product_router)
router.include_router(category_router)
router.include_router(article_router)
router.include_router(filter_router)
router.include_router(sorted_router)
router.include_router(delivery_router)
router.include_router(characteristic_router)
