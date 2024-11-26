from typing import Optional

import cloudinary
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Web Backend"  # Nom de l'application
    APP_VERSION: str = "1.0.0"  # Version de l'application
    ENVIRONMENT: str = "DEV"  # Environnement : DEV ou PROD

    # Base de données
    POSTGRES_URL: Optional[str] = None  # URL de connexion à PostgreSQL

    # JWT Token
    SECRET_KEY: str = (
        "e6b5353c63fe69574c0f456b514423a1"  # Utilisez un générateur sécurisé pour produire une clé
    )
    ALGORITHM: str = "HS256"  # Algorithme utilisé pour signer le token
    ACCESS_TOKEN_EXPIRE_MINUTES: int  # Durée de validité du token (en minutes)
    # Logging
    LOG_LEVEL: str = "DEBUG"  # Niveau de log par défaut
    LOG_FILE: str = "application"

    # Configurations Cloudinary
    CLOUDINARY_CLOUD_NAME: str  # Nom du cloud Cloudinary, doit être fourni dans `.env`
    CLOUDINARY_API_KEY: str  # API Key Cloudinary, doit être fourni dans `.env`
    CLOUDINARY_API_SECRET: str  # API Secret Cloudinary, doit être fourni dans `.env`

    # Configuration de Pydantic
    model_config = SettingsConfigDict(
        env_file=".env"
    )  # Charger les variables d'environnement depuis .env


# Instancier les paramètres une seule fois pour l'ensemble du projet
settings = Settings()
# Configurer Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)
