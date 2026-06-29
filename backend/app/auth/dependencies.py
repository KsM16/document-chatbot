# backend/app/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database.supabase import supabase_service_role

# FastAPI built-in security scheme to extract the Bearer token from headers
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Verifies the Supabase JWT and returns the user payload.
    Raises 401 if the token is missing, invalid, or expired.
    """
    token = credentials.credentials
    
    try:
        # Use the service role client to verify the user's token
        user_response = supabase_service_role.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
            
        # Return the user object as a dictionary
        return user_response.user.model_dump()
        
    except Exception as e:
        # Catch any errors from the Supabase SDK (e.g., expired token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )