from fastapi import APIRouter, status, Response, Request, HTTPException, Form
from starlette.responses import HTMLResponse

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


@router.put("/update_info", response_model=Message, status_code=status.HTTP_200_OK)
async def update_user_info(request: Request, user_update: UpdateUserInfoRequest):
    return await UserService.update_user_info(request, user_update)



@router.delete("/delete_me", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_me(request: Request, response: Response):
    return await UserService.delete_account(request=request, response=response)


@router.put("/change_role/{new_role}", response_model=Message, status_code=status.HTTP_200_OK)
async def change_role(new_role: str, request: Request, response: Response):
    return await UserService.change_role(new_role, request, response)


@router.post("/request_password_reset", response_model=Message, status_code=status.HTTP_200_OK)
async def request_password_reset(email: str):
    return await UserService.request_password_reset(email)


@router.get("/reset_password/{token}")
async def reset_password_get(token: str, request: Request):
    html_content = f"""
    <html>
        <head>
            <title>Сброс пароля</title>
        </head>
        <body>
            <h1>Сброс пароля</h1>
            <form action="/api/user/reset_password/{token}" method="post">
                <label for="new_password">Новый пароль:</label><br>
                <input type="password" id="new_password" name="new_password"><br>
                <label for="re_new_password">Повторите новый пароль:</label><br>
                <input type="password" id="re_new_password" name="re_new_password"><br>
                <input type="submit" value="Сбросить пароль">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@router.post("/reset_password/{token}", response_model=Message, status_code=status.HTTP_200_OK)
async def reset_password_post(token: str, new_password: str = Form(...), re_new_password: str = Form(...)):
    if new_password != re_new_password:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    return await UserService.reset_password(token, new_password)


