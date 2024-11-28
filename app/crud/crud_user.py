from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.schemas.schema_user import UserCreate, UserUpdate


class DuplicateUserError(Exception):
    def __init__(self, message="Username ou email déjà utilisé."):
        """
        Initialiser l'exception DuplicateUserError.

        Args:
            message (str): Le message d'erreur.
        """
        super().__init__(message)


class CRUDUser:

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """
        Récupérer un utilisateur par son ID.
        """
        return db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Récupérer un utilisateur par son nom d'utilisateur.
        """
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Récupérer un utilisateur par son email.
        """
        return db.query(User).filter(User.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Récupérer une liste d'utilisateurs avec pagination.
        """
        return db.query(User).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        """
        Créer un utilisateur avec gestion des doublons explicite.
        """
        existing_user = (
            db.query(User)
            .filter((User.username == obj_in.username) | (User.email == obj_in.email))
            .first()
        )

        if existing_user:
            raise DuplicateUserError()

        new_user = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=obj_in.hashed_password,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
            role=obj_in.role,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Mettre à jour un utilisateur existant.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, user_id: int) -> Optional[User]:
        """
        Supprimer un utilisateur par son ID.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return user

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        """
        Authentifier un utilisateur en comparant le mot de passe haché.
        """
        user = self.get_by_username(db, username)
        if user and self.verify_password(password, user.hashed_password):
            return user
        return None

    def is_superuser(self, user: User) -> bool:
        """
        Vérifier si l'utilisateur est un superutilisateur.
        """
        return user.is_superuser

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Vérifier le mot de passe (implémentez cette méthode avec votre fonction de hashage).
        """
        # Implémentez ici la vérification de mot de passe avec votre méthode de hashage
        from app.utils.security import verify_password as verify_password_hash

        return verify_password_hash(plain_password, hashed_password)

    def set_password(self, user: User, plain_password: str):
        """
        Définir un mot de passe pour un utilisateur.
        """
        from app.utils.security import get_password_hash

        user.hashed_password = get_password_hash(plain_password)


# Initialisation d'une instance CRUDUser
crud_user = CRUDUser()
