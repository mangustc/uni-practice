from fastapi import APIRouter, status, Response, Request, Query
from schemas import *
from services import ProductService



router = APIRouter(tags=["Delivery"])

@router.get(
    "/delivery_services/{delivery_service_id}", response_model=DeliveryServiceResponse
)
async def get_delivery_service(delivery_service_id: int):
    return await ProductService.get_delivery_service(delivery_service_id)


@router.get("/delivery_services", response_model=List[DeliveryServiceResponse])
async def list_delivery_services():
    return await ProductService.list_delivery_services()


@router.post(
    "/delivery_services", response_model=DeliveryServiceResponse, status_code=status.HTTP_201_CREATED
)
async def create_delivery_service(
    request: Request, delivery_service: DeliveryServiceCreate
):
    return await ProductService.create_delivery_service(request, delivery_service)

