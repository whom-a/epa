"""
Service Methods for API

Functions are called here if their name is specified as
an operationId in the OpenAPI specification.
"""

from epa_api.apis.default_api_base import BaseDefaultApi
from epa_api.models.status import Status

class EpaAPIImplementation(BaseDefaultApi):
    async def get_status(self) -> Status:
        return Status(status="healthy", version="1.0.0")