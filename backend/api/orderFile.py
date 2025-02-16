from fastapi import APIRouter, UploadFile, File, status, Response, Request, Query
from schemas import *
from services import OrderService

router = APIRouter(tags=["Order"], prefix="/order")


@router.post("/orders", response_model=PlaceOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(request: Request, order_request: PlaceOrderRequest):
    return await OrderService.place_order(request=request, order_request=order_request)


@router.get("/history_orders", response_model=list[OrderHistoryResponse], status_code=status.HTTP_200_OK)
async def order_history(request: Request):
    return await OrderService.get_order_history(request=request)


@router.put("/pay/{order_id}", response_model=PayOrderResponse, status_code=status.HTTP_200_OK)
async def pay_order(request: Request, order_id: int, pay: bool):
    return await OrderService.pay_order(request=request, order_id=order_id, pay=pay)
