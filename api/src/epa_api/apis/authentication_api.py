# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from epa_api.apis.authentication_api_base import BaseAuthenticationApi
import epa_api.api_implementation

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from epa_api.models.extra_models import TokenModel  # noqa: F401
from epa_api.models.apple_token_exchange import AppleTokenExchange
from epa_api.models.auth_token import AuthToken
from epa_api.models.login_request import LoginRequest
from epa_api.models.social_token_exchange import SocialTokenExchange
from epa_api.models.user_created import UserCreated
from epa_api.models.user_registration import UserRegistration
from epa_api.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = epa_api.api_implementation
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/v1/auth/register",
    responses={
        200: {"model": UserCreated, "description": "User created successfully"},
    },
    tags=["Authentication"],
    summary="Register a new user",
    response_model_by_alias=True,
)
async def register_new_user(
    user_registration: UserRegistration = Body(None, description=""),
) -> UserCreated:
    """Creates a user account. Users must be authenticated via email to avoid spam."""
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().register_new_user(user_registration)


@router.post(
    "/v1/auth/login",
    responses={
        200: {"model": AuthToken, "description": "Successful authentication returns access and a session token."},
    },
    tags=["Authentication"],
    summary="Login with email/password",
    response_model_by_alias=True,
)
async def login_with_password(
    login_request: LoginRequest = Body(None, description=""),
) -> AuthToken:
    """Returns a JWT for application access."""
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().login_with_password(login_request)


@router.post(
    "/v1/auth/social/google",
    responses={
        200: {"model": AuthToken, "description": "Successful authentication returns access and session token."},
    },
    tags=["Authentication"],
    summary="Google OAuth2 Exchange",
    response_model_by_alias=True,
)
async def authenticate_with_google(
    social_token_exchange: SocialTokenExchange = Body(None, description=""),
) -> AuthToken:
    """Exchanges a Google ID Token for an EPA-issued JWT."""
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().authenticate_with_google(social_token_exchange)


@router.post(
    "/v1/auth/social/apple",
    responses={
        200: {"model": AuthToken, "description": "Successful authentication returns access and session token."},
    },
    tags=["Authentication"],
    summary="Apple Sign-In Exchange",
    response_model_by_alias=True,
)
async def authenticate_with_apple(
    apple_token_exchange: AppleTokenExchange = Body(None, description=""),
) -> AuthToken:
    """Exchanges an Apple Identity Token for an EPA-issued JWT."""
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().authenticate_with_apple(apple_token_exchange)


@router.post(
    "/v1/auth/session",
    responses={
        200: {"model": AuthToken, "description": "Successful authentication returns access and a session token."},
    },
    tags=["Authentication"],
    summary="Session Token Renewal",
    response_model_by_alias=True,
)
async def renew_session_token(
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> AuthToken:
    """Uses a session token to generate a new short-lived access JWT."""
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().renew_session_token()
