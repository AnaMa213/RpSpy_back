from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models import CampaignSession
from app.schemas import SessionCreate, SessionUpdate


class CRUDSession:
    def get_by_id(self, db: Session, session_id: int) -> Optional[CampaignSession]:
        """
        Récupérer une session par son ID.
        """
        return (
            db.query(CampaignSession).filter(CampaignSession.id == session_id).first()
        )

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[CampaignSession]:
        """
        Récupérer une liste de sessions avec pagination.
        """
        return db.query(CampaignSession).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: SessionCreate) -> CampaignSession:
        """
        Créer une nouvelle session.
        """
        session = CampaignSession(
            title=obj_in.title,
            date=obj_in.date,
            description=obj_in.description,
            audio_path=obj_in.audio_path,
            campaign_id=obj_in.campaign_id,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def update(
        self, db: Session, db_obj: CampaignSession, obj_in: SessionUpdate
    ) -> CampaignSession:
        """
        Mettre à jour une session existante.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, session_id: int) -> Optional[CampaignSession]:
        """
        Supprimer une session par son ID.
        """
        session = (
            db.query(CampaignSession).filter(CampaignSession.id == session_id).first()
        )
        if session:
            db.delete(session)
            db.commit()
        return session

    def add_player(self, db: Session, session: CampaignSession, player_id: int):
        """
        Ajouter un joueur à une session.
        """
        if player_id not in [player.id for player in session.players]:
            session.players.append(player_id)
            db.commit()

    def remove_player(self, db: Session, session: CampaignSession, player_id: int):
        """
        Retirer un joueur d'une session.
        """
        session.players = [
            player for player in session.players if player.id != player_id
        ]
        db.commit()

    def add_npc(self, db: Session, session: CampaignSession, npc_id: int):
        """
        Ajouter un PNJ à une session.
        """
        if npc_id not in [npc.id for npc in session.npcs]:
            session.npcs.append(npc_id)
            db.commit()

    def remove_npc(self, db: Session, session: CampaignSession, npc_id: int):
        """
        Retirer un PNJ d'une session.
        """
        session.npcs = [npc for npc in session.npcs if npc.id != npc_id]
        db.commit()


# Initialisation de l'instance CRUDSession
crud_session = CRUDSession()
