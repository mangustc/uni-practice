from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import UserService

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/register", response_model=RegistrResponse, status_code=status.HTTP_201_CREATED)
async def register(user: Registr):
    return await UserService.registration(user)


@router.post("/register_legal_entity", response_model=RegistrResponse, status_code=status.HTTP_201_CREATED)
async def register_legal_entity(user: RegistrLegalEntity):
    return await UserService.registration_legal_entity(user)


@router.post("/register_ip", response_model=RegistrResponse, status_code=status.HTTP_201_CREATED)
async def register_ip(user: RegistrLegalEntity):
    return await UserService.registration_ip(user)


@router.put("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(login_data: Login, response: Response):
    return await UserService.login(login_data, response)


@router.post("/logout", response_model=Message, status_code=status.HTTP_200_OK)
async def logout(response: Response):
    return await UserService.logout(response)


@router.put("/name", response_model=Message, status_code=status.HTTP_200_OK)
async def update_name(name: str, request: Request):
    return await UserService.update_name(name, request)


@router.put("/surname", response_model=Message, status_code=status.HTTP_200_OK)
async def update_surname(surname: str, request: Request):
    return await UserService.update_surname(surname, request)


@router.get("/me", response_model=GetUserInfoResponse, status_code=status.HTTP_200_OK)
async def get_user_info(request: Request):
    return await UserService.get_user_info(request)


@router.delete("/delete_me", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_me(request: Request, response: Response):
    return await UserService.delete_account(request=request, response=response)


@router.put("/change_role/{new_role}", response_model=Message, status_code=status.HTTP_200_OK)
async def change_role(new_role: str, request: Request, response: Response):
    return await UserService.change_role(new_role, request, response)