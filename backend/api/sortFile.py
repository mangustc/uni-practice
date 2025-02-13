from fastapi import APIRouter, status
from services import SortService
from schemas import *


router = APIRouter(tags=["Sorts"], prefix="/sort")


@router.get("/products/sort/price/ascending", response_model=List[SortProductByPriceResponse], status_code=status.HTTP_200_OK)
async def sort_products_by_price_ascending_endpoint():
    return await SortService.sort_products_by_price_ascending()


@router.get("/products/sort/price/descending", response_model=List[SortProductByPriceResponse], status_code=status.HTTP_200_OK)
async def sort_products_by_price_descending_endpoint():
    return await SortService.sort_products_by_price_descending()


@router.get("/products/sort/name/ascending", response_model=List[SortProductByNameResponse], status_code=status.HTTP_200_OK)
async def sort_products_by_name_ascending_endpoint():
    return await SortService.sort_products_by_name_ascending()


@router.get("/products/sort/name/descending", response_model=List[SortProductByNameResponse], status_code=status.HTTP_200_OK)
async def sort_products_by_name_descending_endpoint():
    return await SortService.sort_products_by_name_descending()