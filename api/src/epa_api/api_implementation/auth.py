"""
Service Methods for API Auth Endpoints

Functions are called here if their name is specified as
an operationId in the OpenAPI specification.
"""

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from epa_api.apis.authentication_api_base import BaseAuthenticationApi
from epa_api.models.user_registration import UserRegistration
from epa_api.api_implementation.utils.mongo import MongoUtils
from fastapi import status

class AuthAPIImplementation(BaseAuthenticationApi):
    async def register_new_user(self, user_registration: UserRegistration):
        
        # Verify that payload is valid for user registration
        if not user_registration or not user_registration.validate:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            
        # Check that username is at least 8 characters
        if len(user_registration.username) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be at least 8 characters")
            
        # Check that password is at least 12 characters
        if len(user_registration.password) < 12:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 12 characters")

        # Get MongoDB connection
        db = MongoUtils.get_mongodb_database_connection()
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={}
        )