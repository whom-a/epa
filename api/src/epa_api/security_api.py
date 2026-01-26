# coding: utf-8
from fastapi import Depends, Security, status  # noqa: F401
from fastapi.exceptions import HTTPException
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows  # noqa: F401
from fastapi.security import (  # noqa: F401
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi.security.api_key import APIKeyCookie, APIKeyHeader, APIKeyQuery  # noqa: F401
from epa_api.models.extra_models import TokenModel
from epa_api.api_implementation.utils.token import TokenUtils

bearer_auth = HTTPBearer()

def get_token_BearerAuth(credentials: HTTPAuthorizationCredentials = Depends(bearer_auth)) -> TokenModel:
    """
    Check and retrieve authentication information from custom bearer token.

    :param credentials Credentials provided by Authorization header
    :type credentials: HTTPAuthorizationCredentials
    :return: Decoded token information or None if token is invalid
    :rtype: TokenMode
    """

    if TokenUtils.is_token_valid(credentials.credentials):
        output = TokenModel(sub=credentials.credentials)
        return output
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

