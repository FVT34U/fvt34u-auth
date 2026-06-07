from fastapi import APIRouter, Depends
from models import LoginRequest, RegisterRequest, UserResponse
from core.dependencies import get_auth_service
from services import AuthService


router = APIRouter(prefix="/auth")


@router.post("/login", status_code=200, response_model=UserResponse)
async def login(
    body: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.login(body)
    return user


@router.post("/register", status_code=201, response_model=UserResponse)
async def register(
    body: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.register(body)
    return user


@router.get("/logout")
async def logout():
    pass


@router.get("/refresh")
async def refresh():
    pass