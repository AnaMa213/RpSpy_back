# Permet d'importer tous les endpoints depuis app.api.routes

from .endpoints.user_controller import router as user_controller

__all__ = ["user_controller"]
