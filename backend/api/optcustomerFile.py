from schemas import *
from fastapi import APIRouter, status, Request

from services import WholesaleBuyerService

router = APIRouter(tags=["OptCustomer"], prefix="/optcustomer")

@router.post("/create_wholesale_buyer", response_model=WholesaleBuyerResponse, status_code=status.HTTP_201_CREATED)
async def create_wholesale_buyer(wholesale_buyer: WholesaleBuyerCreate):
    return await WholesaleBuyerService.create_wholesale_buyer(wholesale_buyer)
