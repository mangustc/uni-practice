import json

from fastapi import APIRouter, status, Response, Request, Query, HTTPException
from schemas import *
from services import FilterService
from typing import List, Optional

router = APIRouter(tags=["Filters"], prefix="/filter")


class ProductResponse(BaseModel):
    product_id: int
    category_id: int
    category_name: str
    article_id: int
    color_id: Optional[int]
    color_name: Optional[str]
    product_name: str
    product_description: Optional[str]
    product_measured_in: str
    product_amount: float
    product_price: int
    product_new: bool
    product_hit: bool
    product_promotion: bool
    product_percent_promotion: Optional[float]
    product_new_price: Optional[float]


@router.get("get_info_for_catalog_page/{category_id}", response_model=CatalogPageInfo)
async def get_info_for_catalog_page(category_id: int, request: Request):
    return await FilterService.get_info_for_catalog_page(category_id, request)


@router.get("/search/", response_model=List[ProductInCatalogInfo])
async def search_products(
        request: Request,
        search_term: str = Query(..., title="Search Term"),
        sort_by: Optional[str] = Query(None, title="Sort By")):
    """- ** sort_by **: Поле для сортировки(например, "price", "name", "-price", "-name"). products"""
    products = await FilterService.search_products_by_name(request, search_term, sort_by)
    return products


@router.post("/products/by-category", response_model=List[ProductInCatalogInfo])
async def get_products_by_category(
        request: Request,
        filters: CatalogFilters,
        sort_by: SortByEnum,
        filter_by_params: FilterByParamsEnum):
    products = await FilterService.get_products_by_category_id(request, filters, sort_by, filter_by_params)
    return products

