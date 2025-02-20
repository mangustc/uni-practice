from api.userAuthFile import router as user_router
from api.productFile import router as product_router
from api.categoryFile import router as category_router
from api.articleFile import router as article_router
from api.filterFile import router as filter_router
from api.delivery import router as delivery_router
from api.classifierFile import router as characteristic_router
from api.cartFile import router as cart_router
from api.orderFile import router as order_router
from api.feedbackFile import router as feedback_router
from api.vacancyFile import router as vacancy_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(user_router)
router.include_router(product_router)
router.include_router(category_router)
router.include_router(article_router)
router.include_router(filter_router)
router.include_router(delivery_router)
router.include_router(characteristic_router)
router.include_router(cart_router)
router.include_router(order_router)
router.include_router(feedback_router)
router.include_router(vacancy_router)
