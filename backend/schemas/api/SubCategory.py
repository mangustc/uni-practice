from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import SubcategoryService

router = APIRouter(tags=["Subcategory"], prefix="/subcategory")



@router.post("/AddSubcategory", response_model=SubcategoryResponse)
async def add_subcategory(subcategory: AddSubcategory, request: Request):
    return await SubcategoryService.add_subcategory(subcategory, request)


@router.get("/GetSubcategory/{subcategory_id}")
async def get_subcategory(subcategory_id: int):
    return await SubcategoryService.get_subcategory(subcategory_id)


@router.get("/GetAllSubcategories")
async def get_all_subcategories():
    return await SubcategoryService.get_all_subcategories()


@router.put("/UpdateSubcategory/{subcategory_id}", response_model=SubcategoryResponse)
async def update_subcategory(subcategory_id: int, new_name: str, request: Request, category_id: int):
    return await SubcategoryService.update_subcategory(
        subcategory_id, new_name, request, category_id
    )


@router.delete("/DeleteSubcategory/{subcategory_id}")
async def delete_subcategory(subcategory_id: int, request: Request):
    return await SubcategoryService.delete_subcategory(subcategory_id, request)