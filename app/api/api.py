from fastapi import APIRouter

from app.api.endpoints import campaign_controller as campaigns
from app.api.endpoints import dialog_controller as dialogs
from app.api.endpoints import npc_controller as npcs
from app.api.endpoints import player_controller as players
from app.api.endpoints import session_controller as sessions
from app.api.endpoints import user_controller as users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["Campaigns"])
api_router.include_router(players.router, prefix="/players", tags=["Players"])
api_router.include_router(npcs.router, prefix="/npcs", tags=["NPCs"])
api_router.include_router(dialogs.router, prefix="/dialogs", tags=["Dialogs"])
