from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import CategoryService

router = APIRouter(tags=["Category"], prefix="/category")


@router.post("/add_category_root", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def add_category_root(category: AddCategoryRoot, request: Request):
    return await CategoryService.add_category_root(category, request)


@router.post("/add_category", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def add_category(category: AddCategory, request: Request):
    return await CategoryService.add_category(category, request)


@router.get("/get_category/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category(category_id: int):
    return await CategoryService.get_category(category_id)


@router.get("/get_category_roots", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_category_roots():
    return await CategoryService.get_category_roots()


@router.get("/get_categories_by_category_name_refers_to/{category_name_parent}", response_model=list[CategoryResponse],
            status_code=status.HTTP_200_OK)
async def get_categories_by_category_name_parent(category_name_parent: str):
    return await CategoryService.get_categories_by_category_name_parent(category_name_parent)


@router.get("/get_all_categories", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories():
    return await CategoryService.get_all_categories()


@router.put("/update_category/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(category_id: int, new_name: str, request: Request):
    return await CategoryService.update_category(category_id, new_name, request)


@router.delete("/delete_category/{category_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, request: Request):
    return await CategoryService.delete_category(category_id, request)
