from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.schemas.schema_user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user_role(token: str = Depends(oauth2_scheme)) -> UserRole:
    """
    Gets the current user role from the Authorization Bearer token.

    Args:
        token (str): The Authorization Bearer token.

    Returns:
        UserRole: The current user role.

    Raises:
        HTTPException: If the token is invalid, expired, or missing the role.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        role = payload.get("role")
        if role is None:
            raise credentials_exception
        return UserRole(role)
    except JWTError as exc:
        raise credentials_exception from exc


def require_role(required_role: UserRole):
    """
    Decorator to require a specific role to access a route.

    Args:
        required_role (UserRole): The required role.

    Returns:
        Depends: A dependency that will check the user role.

    Raises:
        HTTPException: If the user role does not match the required role.
    """

    def role_dependency(current_role: UserRole = Depends(get_current_user_role)):
        if current_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )

    return Depends(role_dependency)


# Fonction pour vérifier le token
def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verify the JWT token and return the payload.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict: The payload of the JWT token.

    Raises:
        HTTPException: If the token is invalid or has expired.
    """

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
