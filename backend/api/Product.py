from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import ProductService

router = APIRouter(tags=["Product"], prefix="/product")

@router.post("/AddProduct")
async def add_product(product: ProductInformation):
    return await ProductService.add_inform_product(product)