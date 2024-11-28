from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud_user import crud_user
from app.utils.security import create_access_token, verify_password


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        """
        Authentifie un utilisateur en vérifiant le mot de passe.
        """
        user = crud_user.get_by_username(db, username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def login(db: Session, username: str, password: str):
        """
        Authentifie un utilisateur, génère un token JWT et retourne les informations d'authentification.
        """
        # Authentification de l'utilisateur
        user = AuthService.authenticate_user(db, username, password)
        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        # Génération du token d'accès
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role.value},
            expires_delta=access_token_expires,
        )

        # Retour des données d'authentification
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role.value,
        }
