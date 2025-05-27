# app/auth/dependencies.py

from fastapi import Depends, HTTPException, status, Header
from app.auth.auth_handler import decode_token


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    token = authorization.split(" ")[1]
    user = decode_token(token)
    return user


def require_role(allowed_roles: list):
    def role_dependency(current_user=Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_dependency
