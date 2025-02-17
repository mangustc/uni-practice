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

# @router.get("/{category_name}", response_model=List[ProductResponse])
# async def get_filter_products(
#         category_name: str,
#         filters: Optional[str] = Query(None),  # JSON строка с фильтрами
#         sort_by: Optional[str] = Query(None),  # Поле для сортировки
#         filter_by_params: Optional[str] = Query(None)  # Фильтрация по hit, promotion, new
# ):
#     """
#     Получение товаров по имени категории с возможностью фильтрации и сортировки.
#
#     - **category_name**: Название категории товаров.
#     - **filters**: JSON строка с фильтрами по характеристикам ({"property_id": "value"}).
#     - **sort_by**: Поле для сортировки (например, "price", "name", "-price", "-name").
#     - **filter_by_params**: Фильтрация по параметрам (hit, promotion, new).
#     """
#     # Преобразуем JSON строку в словарь, если она есть
#     filters_dict = None
#     if filters:
#         try:
#             filters_dict = json.loads(filters)
#         except json.JSONDecodeError:
#             raise HTTPException(status_code=400, detail="Invalid JSON format for filters")
#
#     products = await FilterService.get_products_by_category_name_true(category_name, filters_dict, sort_by, filter_by_params)
#
#     return products

@router.get("test/{category_name}", response_model=List[ProductResponse])
async def get_filter_products_test(
        category_name: str,
        filters: Optional[str] = Query(None),  # JSON строка с фильтрами
        sort_by: Optional[str] = Query(None),  # Поле для сортировки
        filter_by_params: Optional[str] = Query(None)  # Фильтрация по hit, promotion, new
):
    """
    Получение товаров по имени категории с возможностью фильтрации и сортировки.

    - **category_name**: Название категории товаров.
    - **filters**: JSON строка с фильтрами по характеристикам ({"property_id": "value", "color_name": "Синий"}).
    - **sort_by**: Поле для сортировки (например, "price", "name", "-price", "-name").
    - **filter_by_params**: Фильтрация по параметрам (hit, promotion, new).
    """
    # Преобразуем JSON строку в словарь, если она есть
    filters_dict = None
    if filters:
        try:
            filters_dict = json.loads(filters)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format for filters")

    products = await FilterService.get_products_by_category_name_test(category_name, filters_dict, sort_by, filter_by_params)

    return products


@router.get("/search/", response_model=List[ProductResponse])
async def search_products(search_term: str = Query(..., title="Search Term"), sort_by: Optional[str] = Query(None, title="Sort By")):
    """- ** sort_by **: Поле для сортировки(например, "price", "name", "-price", "-name"). products"""
    products = await FilterService.search_products_by_name(search_term, sort_by)
    return products
