from fastapi import APIRouter
from services import SortService


router = APIRouter(tags=["Sorts"], prefix="/sort")


@router.get("/products/sort/price/ascending")
async def sort_products_by_price_ascending_endpoint():
    return await SortService.sort_products_by_price_ascending()


@router.get("/products/sort/price/descending")
async def sort_products_by_price_descending_endpoint():
    return await SortService.sort_products_by_price_descending()


@router.get("/products/sort/name/ascending")
async def sort_products_by_name_ascending_endpoint():
    return await SortService.sort_products_by_name_ascending()


@router.get("/products/sort/name/descending")
async def sort_products_by_name_descending_endpoint():
    return await SortService.sort_products_by_name_descending()