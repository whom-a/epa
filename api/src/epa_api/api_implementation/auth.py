"""
Service Methods for API Auth Endpoints

Functions are called here if their name is specified as
an operationId in the OpenAPI specification.
"""

from fastapi.exceptions import HTTPException
from epa_api.apis.authentication_api_base import BaseAuthenticationApi
from epa_api.models.user_registration import UserRegistration
from epa_api.models.user_created import UserCreated
from epa_api.models.login_request import LoginRequest
from epa_api.models.auth_token import AuthToken
from epa_api.api_implementation.utils.mongo import MongoUtils
from epa_api.api_implementation.utils.user import UserUtils
from epa_api.api_implementation.utils.token import TokenUtils
from epa_api.api_implementation.utils.context import current_token_data
from fastapi import status

class AuthAPIImplementation(BaseAuthenticationApi):
    async def register_new_user(self, user_registration: UserRegistration) -> UserCreated:
        
        # Verify that payload is valid for user registration
        if not user_registration or not user_registration.model_validate:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            
        # Check that username is at least 8 characters
        if len(user_registration.username) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be at least 6 characters")
            
        # Check that password is at least 12 characters
        if len(user_registration.password) < 12:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 12 characters")
            
        # Connect to the database
        client, db = MongoUtils.get_mongodb_database_connection()
        user_collection = MongoUtils.get_user_collection(db)
        
        # Check that the creds are not taken
        if UserUtils.is_email_taken(user_registration.email, user_collection):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")
        
        if UserUtils.is_username_taken(user_registration.username, user_collection):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
        
        # Create the user
        user_id = UserUtils.create_standard_user(
            user_registration,
            user_collection
        )
        
        client.close()
        return UserCreated(user_id=user_id)
        
    async def login_with_password(self, login_request: LoginRequest) -> AuthToken:
        
        # Verify that payload is valid for user login
        if not login_request.model_validate:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
        email = login_request.email
        password = login_request.password
        
        client, db = MongoUtils.get_mongodb_database_connection()
        user_collection = MongoUtils.get_user_collection(db)
        
        user = UserUtils.get_user_from_email(email, user_collection)
        if not user or not UserUtils.verify_password(password, user["password"], user["salt"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
        new_access_token = TokenUtils.generate_new_access_token(user, user_collection)
        new_session_token = TokenUtils.generate_new_session_token(user, MongoUtils.get_session_tokens_collection(db))
        client.close()
        
        return AuthToken(
            access_token=new_access_token,
            session_token=new_session_token,
            token_type="Bearer",
            expires_in=TokenUtils.get_ttl_in_seconds(TokenUtils.get_expire_date(new_access_token))
        )
        
    async def renew_session_token(self) -> AuthToken:
        
        token = current_token_data.get()
        
        # This should never be executed since the security api handles invalid tokens
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Token lost")
            
        client, db = MongoUtils.get_mongodb_database_connection()
        user_collection = MongoUtils.get_user_collection(db)
        user = UserUtils.get_user_from_user_id(TokenUtils.get_user_id(token.sub), user_collection)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
        new_access_token = TokenUtils.generate_new_access_token(user, user_collection)
        client.close()
        
        return AuthToken(
            access_token=new_access_token,
            session_token=token.sub,
            token_type="Bearer",
            expires_in=TokenUtils.get_ttl_in_seconds(TokenUtils.get_expire_date(new_access_token))
        )