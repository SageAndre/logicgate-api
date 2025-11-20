from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# In a real app, this comes from an Environment Variable
API_KEY = "logicgate-secret-key"
API_KEY_NAME = "X-API-KEY"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials"
    )