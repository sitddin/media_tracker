import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:

    auth_error = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if credentials is None:
        raise auth_error

    try:
        user_id = decode_access_token(credentials.credentials)
    except (jwt.PyJWTError, ValueError, KeyError, TypeError):
        raise auth_error

    user = db.get(User, user_id)

    if user is None:
        raise auth_error

    return user