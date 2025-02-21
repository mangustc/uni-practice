from fastapi import APIRouter, status, Response, Request, Query
from schemas import *
from services import DeliveryServices


router = APIRouter(tags=["Delivery"])


@router.get("/delivery_services/{delivery_service_id}", response_model=DeliveryServiceResponse)
async def get_delivery_service(delivery_service_id: int):
    return await DeliveryServices.get_delivery_service(delivery_service_id)


@router.get("/delivery_services", response_model=List[DeliveryServiceResponse])
async def list_delivery_services():
    return await DeliveryServices.list_delivery_services()


@router.post("/delivery_services", response_model=DeliveryServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery_service(request: Request, delivery_service: DeliveryServiceCreate):
    return await DeliveryServices.create_delivery_service(request, delivery_service)


@router.put("/delivery_services_update/{delivery_id}", response_model=DeliveryServiceResponse, status_code=status.HTTP_201_CREATED)
async def update_delivery_service(request: Request, delivery_id: int, delivery_service: DeliveryUpdate):
    return await DeliveryServices.update_delivery_service(request, delivery_id, delivery_service)


@router.delete("/delivery_services_delete/{delivery_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_delivery_service(request: Request, delivery_id: int):
    return await DeliveryServices.delete_delivery(request, delivery_id)