from fastapi import APIRouter, UploadFile, File, status, Response, Request
from schemas import *
from services import ProductService

router = APIRouter(tags=["Product"], prefix="/product")


@router.post("/CreateProduct")
async def create_product(request: Request, data: CreateProduct):
    return await ProductService.create_product(request, data)


@router.get("/{product_id}/GetProduct")
async def get_product(product_id: int):
    return await ProductService.get_product(product_id)


@router.get("/{product_id}/GetProductSmallCard")
async def get_product_small_card(product_id: int):
    return await ProductService.get_product_small_card(product_id)


@router.get("/GetAllProducts")
async def get_all_products():
    return await ProductService.get_all_products()


@router.get("/{product_id}/GetPhoto")
async def get_product_photo(product_id):
    return await ProductService.get_product_photo(product_id)


@router.put("/{product_id}/UpdatePhoto")
async def update_product_photo(request: Request, product_id: int, file: UploadFile = File(...)):
    return await ProductService.update_product_photo(request, product_id, file)


@router.put("/{product_id}/Update")
async def update_product_information(request: Request, product_id: int, data: CreateProduct):
    return await ProductService.update_product_information(request, product_id, data)


@router.delete("/{product_id}/Delete")
async def delete_product(request: Request, product_id: int):
    return await ProductService.delete_product(request, product_id)
