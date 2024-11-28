from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.db.database import get_db
from app.schemas.schema_token import Token
from app.schemas.schema_user import UserCreate, UserResponse, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/create", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database.

    This endpoint allows for the creation of a new user by accepting
    user details such as email, username, password, and role. It checks
    if the email is already registered, and if not, it creates the user
    with a hashed password.

    Args:
        user (UserCreate): The user details to create the new user.
        db (Session): The database session used for adding the new user.

    Returns:
        User: The newly created user object.

    Raises:
        HTTPException: If the email is already registered.
    """
    try:
        user = crud_user.create(db=db, obj_in=user)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticates a user and returns an access token.

    This function handles user login by verifying the username and password
    provided in the form data. If the authentication is successful, it generates
    a JSON Web Token (JWT) with an expiration time and returns it along with the
    token type and user role.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the
            username and password for authentication.
        db (Session): The database session used for querying user data.

    Returns:
        dict: A dictionary containing the access token, token type, and user role.

    Raises:
        HTTPException: If the username or password is incorrect.
    """
    return AuthService.login(
        db=db, username=form_data.username, password=form_data.password
    )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.get_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    updated_user = crud_user.update(db=db, db_obj=db_user, obj_in=user_in)
    return updated_user
