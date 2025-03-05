from fastapi import APIRouter, UploadFile, File, status, Response, Request, Query
from schemas import *
from services import CartService

router = APIRouter(tags=["Cart"], prefix="/cart")


@router.post("/add_in_cart/{product_id}/{amount}", response_model=Message, status_code=status.HTTP_201_CREATED)
async def add_in_cart(request: Request, product_id: int, amount: float, response: Response):
    return await CartService.add_in_cart(request, product_id, amount, response)


@router.get("/get_user_cart", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_user_cart(request: Request, response: Response):
    return await CartService.get_user_cart(request, response)


@router.put("/change_amount_in_cart/{product_id}/{amount}", response_model=Message, status_code=status.HTTP_200_OK)
async def change_product_amount_in_cart(request: Request, product_id: int, amount: float, response: Response):
    return await CartService.change_product_amount_in_cart(request, product_id, amount, response)


@router.delete("/delete_from_cart/{product_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_from_cart(request: Request, product_id: int, response: Response):
    return await CartService.delete_from_cart(request, product_id, response)


@router.delete("/clear_cart", response_model=Message, status_code=status.HTTP_200_OK)
async def clear_cart(request: Request, response: Response):
    return await CartService.clear_cart(request, response)
