from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.schemas.blog import TokenOut
from app.services.auth import create_access_token, verify_password

router = APIRouter(prefix="/admin", tags=["admin-auth"])


@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    if form.username != settings.admin_username or not verify_password(
        form.password, _hashed_admin_password()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": form.username})
    return TokenOut(access_token=token)


def _hashed_admin_password() -> str:
    """Return a bcrypt hash of the configured admin password.

    The hash is computed once and cached on first call so we don't rehash on
    every login request.
    """
    if not hasattr(_hashed_admin_password, "_cache"):
        from app.services.auth import hash_password
        _hashed_admin_password._cache = hash_password(settings.admin_password)
    return _hashed_admin_password._cache
