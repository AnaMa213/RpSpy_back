from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.npc import NPC
from app.schemas.schema_npc import NPCCreate, NPCUpdate


class CRUDNPC:
    def get_by_id(self, db: Session, npc_id: int) -> Optional[NPC]:
        """
        Récupérer un PNJ par son ID.
        """
        return db.query(NPC).filter(NPC.id == npc_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[NPC]:
        """
        Récupérer une liste de PNJs avec pagination.
        """
        return db.query(NPC).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: NPCCreate) -> NPC:
        """
        Créer un nouveau PNJ.
        """
        npc = NPC(
            name=obj_in.name,
            race=obj_in.race,
            class_name=obj_in.class_name,
            alignment=obj_in.alignment,
            level=obj_in.level,
            strength=obj_in.strength,
            dexterity=obj_in.dexterity,
            constitution=obj_in.constitution,
            intelligence=obj_in.intelligence,
            wisdom=obj_in.wisdom,
            charisma=obj_in.charisma,
            description=obj_in.description,
        )
        db.add(npc)
        db.commit()
        db.refresh(npc)
        return npc

    def update(self, db: Session, db_obj: NPC, obj_in: NPCUpdate) -> NPC:
        """
        Mettre à jour un PNJ existant.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, npc_id: int) -> Optional[NPC]:
        """
        Supprimer un PNJ par son ID.
        """
        npc = db.query(NPC).filter(NPC.id == npc_id).first()
        if npc:
            db.delete(npc)
            db.commit()
        return npc

    def add_campaign(self, db: Session, npc: NPC, campaign_id: int):
        """
        Ajouter une campagne à un PNJ.
        """
        if campaign_id not in [campaign.id for campaign in npc.campaigns]:
            npc.campaigns.append(campaign_id)
            db.commit()

    def remove_campaign(self, db: Session, npc: NPC, campaign_id: int):
        """
        Retirer une campagne d'un PNJ.
        """
        npc.campaigns = [
            campaign for campaign in npc.campaigns if campaign.id != campaign_id
        ]
        db.commit()

    def add_session(self, db: Session, npc: NPC, session_id: int):
        """
        Ajouter une session à un PNJ.
        """
        if session_id not in [session.id for session in npc.sessions]:
            npc.sessions.append(session_id)
            db.commit()

    def remove_session(self, db: Session, npc: NPC, session_id: int):
        """
        Retirer une session d'un PNJ.
        """
        npc.sessions = [session for session in npc.sessions if session.id != session_id]
        db.commit()


# Initialisation de l'instance CRUDNPC
crud_npc = CRUDNPC()
