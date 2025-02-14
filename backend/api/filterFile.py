from fastapi import APIRouter, status, Response, Request, Query
from schemas import *
from services import FilterService
from typing import List, Optional

router = APIRouter(tags=["Filers"], prefix="/filter")


@router.get("/articles/filter", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def filter_articles_endpoint(
    price_min: Optional[int] = Query(None, description="Minimum price"),
    price_max: Optional[int] = Query(None, description="Maximum price"),
    countries: Optional[List[str]] = Query(None, description="List of countries"),
    colors: Optional[List[str]] = Query(None, description="List of colors"),
    widths: Optional[List[str]] = Query(None, description="List of widths"),
    densities: Optional[List[str]] = Query(None, description="List of densities"),
    consists: Optional[List[str]] = Query(None, description="List of consists"),
):
    return await FilterService.filter_products(
        price_min=price_min,
        price_max=price_max,
        countries=countries,
        colors=colors,
        widths=widths,
        densities=densities,
        consists=consists,
    )