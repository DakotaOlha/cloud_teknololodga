import logging
from datetime import timedelta

import sentry_sdk
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.schemas import Token, UserCreate, UserResponse
from src.auth.service import AuthService, get_current_user
from src.core.database import get_db
from src.core.settings import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    logger.info(f"[AUTH][REGISTER] Attempting to register user: {user_data.username}")
    try:
        service = AuthService(session)
        user = await service.register_user(user_data)
        logger.info(f"[AUTH][REGISTER] User registered successfully: {user.username}")
        return user
    except HTTPException as e:
        logger.warning(f"[AUTH][REGISTER] Registration failed: {e.detail}")
        raise
    except Exception as e:
        logger.exception("[AUTH][REGISTER] Unexpected error during registration")
        sentry_sdk.capture_exception(e)
        raise HTTPException(500, "Registration failed")


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    logger.info(f"[AUTH][LOGIN] Login attempt for user: {form_data.username}")
    try:
        service = AuthService(session)
        user = await service.authenticate_user(form_data.username, form_data.password)
        if not user:
            logger.warning(f"[AUTH][LOGIN] Failed login attempt: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = service.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        logger.info(f"[AUTH][LOGIN] User logged in successfully: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("[AUTH][LOGIN] Unexpected error during login")
        sentry_sdk.capture_exception(e)
        raise HTTPException(500, "Login failed")


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    logger.info(f"[AUTH][ME] Fetching user info: {current_user.username}")
    return current_user
