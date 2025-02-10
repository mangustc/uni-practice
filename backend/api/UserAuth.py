from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import UserService

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/register")
async def register(user: Registr):
    return await UserService.registration(user)


@router.post("/register_legal_entity")
async def register_legal_entity(user: RegistrLegalEntity):
    return await UserService.registration_legal_entity(user)


@router.post("/register_ip")
async def register_ip(user: RegistrLegalEntity):
    return await UserService.registration_ip(user)


@router.put("/login")
async def login(login_data: Login, response: Response):
    return await UserService.login(login_data, response)


@router.post("/logout")
async def logout(response: Response):
    return await UserService.logout(response)


@router.put("/name")
async def update_name(name: str, request: Request):
    return await UserService.update_name(name, request)


@router.put("/surname")
async def update_surname(surname: str, request: Request):
    return await UserService.update_surname(surname, request)


@router.get("/me")
async def get_user_info(request: Request):
    return await UserService.get_user_info(request)


@router.delete("/delete_me")
async def delete_me(request: Request, response: Response):
    return await UserService.delete_account(request=request, response=response)


@router.put("/change_role")
async def change_role(change_role_data: str, request: Request):
    return await UserService.change_role(new_role=change_role_data, request=request)
