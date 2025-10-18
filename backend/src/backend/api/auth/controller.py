from .models import LogInRequest, SignUpRequest, UserInfo
from src.backend.dependencies import get_user_service
from src.domain.services import UserService
from fastapi import Response, Depends, Request, HTTPException
from typing import Annotated
from fastapi_controllers import Controller, get, post
from .models import LogInRequest, SignUpRequest, UserInfo


class AuthController(Controller):
    prefix = "/auth"
    tags = ["auth"]

    def __init__(self, user_service: Annotated[UserService, Depends(get_user_service)]) -> None:
        super().__init__()
        self.user_service = user_service

    @get("", response_model=UserInfo)
    async def get_user_info(self, request: Request):
        user_data = await self.user_service.get_user_json(request.cookies.get("token"))
        if user_data is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return user_data

    @post("/login")
    async def login(self, data: LogInRequest, response: Response):
        result = await self.user_service.login(data)
        response.set_cookie("token", result.token, httponly=True, max_age=60 * 60 * 24 * 30)
        return {"message": "OK"}

    @post("/logout")
    async def logout(self, request: Request, response: Response):
        await self.user_service.logout(request.cookies.get("token"))
        response.delete_cookie("token")
        return {"message": "OK"}

    @post("/registration")
    async def registration(self, data: SignUpRequest):
        await self.user_service.signup(data)
        return {"message": "OK"}
