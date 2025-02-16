from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import ClassifierService

router = APIRouter(tags=["Classifier"], prefix="/classifier")


@router.post("/add_property", response_model=GetPropertyResponse, status_code=status.HTTP_201_CREATED)
async def add_property(property_name: AddProperty, request: Request):
    return await ClassifierService.add_property(property_name, request)


@router.post("/add_color", response_model=GetColorResponse, status_code=status.HTTP_201_CREATED)
async def add_color(color_name: AddColor, request: Request):
    return await ClassifierService.add_color(color_name, request)


@router.get("/get_property/{property_id}", response_model=GetPropertyResponse, status_code=status.HTTP_200_OK)
async def get_property(property_id: int):
    return await ClassifierService.get_property(property_id)


@router.get("/get_color/{color_id}", response_model=GetColorResponse, status_code=status.HTTP_200_OK)
async def get_color(color_id: int):
    return await ClassifierService.get_color(color_id)


@router.get("/get_all_properties", response_model=list[GetPropertyResponse], status_code=status.HTTP_200_OK)
async def get_all_properties():
    return await ClassifierService.get_all_properties()


@router.get("/get_all_colors", response_model=list[GetColorResponse], status_code=status.HTTP_200_OK)
async def get_all_colors():
    return await ClassifierService.get_all_colors()


@router.put("/update_property/{property_id}", response_model=GetPropertyResponse, status_code=status.HTTP_200_OK)
async def update_property(property_id: int, new_name: str, request: Request):
    return await ClassifierService.update_property(property_id, new_name, request)


@router.put("/update_color/{color_id}", response_model=GetColorResponse, status_code=status.HTTP_200_OK)
async def update_color(color_id: int, new_name: str, request: Request):
    return await ClassifierService.update_color(color_id, new_name, request)


@router.delete("/delete_property/{property_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_property(property_id: int, request: Request):
    return await ClassifierService.delete_property(property_id, request)


@router.delete("/delete_color/{color_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_color(color_id: int, request: Request):
    return await ClassifierService.delete_color(color_id, request)
