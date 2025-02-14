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


@router.get("/articles/filter/price", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def filter_articles_by_price_endpoint(
    price_min: Optional[int] = Query(None, description="Minimum price"),
    price_max: Optional[int] = Query(None, description="Maximum price"),
):
    return await FilterService.filter_by_price(price_min=price_min, price_max=price_max)


@router.get("/articles/filter/country", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def filter_articles_by_country_endpoint(
    countries: List[str] = Query(None, description="List of countries"),
):
    return await FilterService.filter_by_country(countries=countries)


@router.get("/articles/filter/color", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def filter_articles_by_color_endpoint(
    colors: List[str] = Query(None, description="List of colors"),
):
    return await FilterService.filter_by_color(colors=colors)


@router.get("/articles/filter/width", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def filter_articles_by_width_endpoint(
    widths: List[str] = Query(None, description="List of widths"),
):
    return await FilterService.filter_by_width(widths=widths)


@router.get("/articles/filter/density", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def filter_articles_by_density_endpoint(
    densities: List[str] = Query(None, description="List of densities"),
):
    return await FilterService.filter_by_density(densities=densities)


@router.get("/articles/filter/consist", response_model=List[GetProductResponse], status_code=status.HTTP_200_OK)
async def filter_articles_by_consist_endpoint(
    consists: List[str] = Query(None, description="List of consists"),
):
    return await FilterService.filter_by_consist(consists=consists)