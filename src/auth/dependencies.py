from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import ValidationError

from . import schemas, service, exceptions, models
from ..database import get_db
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> models.User:
    """
    Mendekode token JWT untuk mendapatkan user saat ini.
    Melindungi endpoint yang memerlukan otentikasi.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = schemas.TokenData(email=payload.get("sub"))
        if token_data.email is None:
            raise exceptions.CredentialsException
    except (JWTError, ValidationError):
        raise exceptions.CredentialsException

    user = service.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise exceptions.CredentialsException
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """Memastikan user yang login aktif."""
    if not current_user.is_active:
        raise exceptions.InactiveUserException
    return current_user