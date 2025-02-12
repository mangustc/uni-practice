from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import CategoryService

router = APIRouter(tags=["Category"], prefix="/category")


@router.post("/AddCategory", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def add_category(category: AddCategory, request: Request):
    return await CategoryService.add_category(category, request)


@router.get("/GetCategory/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category(category_id: int):
    return await CategoryService.get_category(category_id)


@router.get("/GetAllCategories", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories():
    return await CategoryService.get_all_categories()


@router.put("/UpdateCategory/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(category_id: int, new_name: str, request: Request):
    return await CategoryService.update_category(category_id, new_name, request)


@router.delete("/DeleteCategory/{category_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, request: Request):
    return await CategoryService.delete_category(category_id, request)
