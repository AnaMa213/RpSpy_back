# Permet d'importer tous les endpoints depuis app.api.routes

from .crud_campaign import *
from .crud_npc import *
from .crud_player import *
from .crud_session import *
from .crud_user import *

__all__ = ["CRUDSession", "CRUDUser", "CRUDCampaign"]
