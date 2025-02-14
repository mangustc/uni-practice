from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import CharacteristicService

router = APIRouter(tags=["Characteristic"], prefix="/characteristic")


@router.post("/AddProperty", response_model=GetPropertyResponse, status_code=status.HTTP_201_CREATED)
async def add_property(property_name: AddProperty, request: Request):
    return await CharacteristicService.add_property(property_name, request)


@router.post("/AddPropertyValue", response_model=GetPropertyValueResponse, status_code=status.HTTP_201_CREATED)
async def add_property_value(property_value: AddPropertyValue, request: Request):
    return await CharacteristicService.add_property_value(property_value, request)


@router.get("/GetPropertyValuesByPropertyName/{property_name}", response_model=list[GetPropertyValueResponse],
            status_code=status.HTTP_200_OK)
async def get_property_values_by_property_name(property_name: str):
    return await CharacteristicService.get_property_values_by_property_name(property_name)


@router.get("/GetPropertyValuesByPropertyValueName/{property_value_name}", response_model=GetPropertyResponse,
            status_code=status.HTTP_200_OK)
async def get_property_by_property_value_name(property_value_name: str):
    return await CharacteristicService.get_property_by_property_value_name(property_value_name)


@router.get("/GetProperty/{property_id}", response_model=GetPropertyResponse, status_code=status.HTTP_200_OK)
async def get_property(property_id: int):
    return await CharacteristicService.get_property(property_id)


@router.get("/GetPropertyValue/{property_value_id}", response_model=GetPropertyValueResponse,
            status_code=status.HTTP_200_OK)
async def get_property_value(property_value_id: int):
    return await CharacteristicService.get_property_value(property_value_id)


@router.get("/GetAllProperties", response_model=list[GetPropertyResponse], status_code=status.HTTP_200_OK)
async def get_all_properties():
    return await CharacteristicService.get_all_properties()


@router.get("/GetAllPropertyValues", response_model=list[GetPropertyValueResponse], status_code=status.HTTP_200_OK)
async def get_all_property_values():
    return await CharacteristicService.get_all_property_values()


@router.put("/UpdateProperty/{property_id}", response_model=GetPropertyResponse, status_code=status.HTTP_200_OK)
async def update_property(property_id: int, new_name: str, request: Request):
    return await CharacteristicService.update_property(property_id, new_name, request)


@router.put("/UpdatePropertyValue/{property_value_id}", response_model=GetPropertyValueResponse,
            status_code=status.HTTP_200_OK)
async def update_property_value(property_value_id: int, new_name: str, request: Request):
    return await CharacteristicService.update_property_value(property_value_id, new_name, request)


@router.delete("/DeleteProperty/{property_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_property(property_id: int, request: Request):
    return await CharacteristicService.delete_property(property_id, request)


@router.delete("/DeletePropertyValue/{property_value_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_property_value(property_value_id: int, request: Request):
    return await CharacteristicService.delete_property_value(property_value_id, request)
