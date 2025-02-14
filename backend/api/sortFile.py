from fastapi import APIRouter, status
from services import SortService
from schemas import *


router = APIRouter(tags=["Sorts"], prefix="/sort")


@router.get("/articles/sort/price/asc", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def sort_articles_by_price_ascending_endpoint():
    return await SortService.sort_products_by_price_ascending()


@router.get("/articles/sort/price/desc", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def sort_articles_by_price_descending_endpoint():
    return await SortService.sort_products_by_price_descending()


@router.get("/articles/sort/name/asc", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def sort_articles_by_name_ascending_endpoint():
    return await SortService.sort_products_by_name_ascending()


@router.get("/articles/sort/name/desc", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def sort_articles_by_name_descending_endpoint():
    return await SortService.sort_products_by_name_descending()