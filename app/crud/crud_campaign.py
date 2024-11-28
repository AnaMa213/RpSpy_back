from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.campaign import Campaign
from app.schemas import CampaignCreate, CampaignUpdate


class CRUDCampaign:
    def get_by_id(self, db: Session, campaign_id: int) -> Optional[Campaign]:
        """
        Récupérer une campagne par son ID.
        """
        return db.query(Campaign).filter(Campaign.id == campaign_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """
        Récupérer une liste de campagnes avec pagination.
        """
        return db.query(Campaign).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CampaignCreate) -> Campaign:
        """
        Créer une nouvelle campagne.
        """
        campaign = Campaign(
            name=obj_in.name,
            genre=obj_in.genre,
            description=obj_in.description,
            map_url=obj_in.map_url,
            status=obj_in.status,
            notes_url=obj_in.notes_url,
            mj_id=obj_in.mj_id,
            created_by=obj_in.created_by,
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign

    def update(self, db: Session, db_obj: Campaign, obj_in: CampaignUpdate) -> Campaign:
        """
        Mettre à jour une campagne existante.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, campaign_id: int) -> Optional[Campaign]:
        """
        Supprimer une campagne par son ID.
        """
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            db.delete(campaign)
            db.commit()
        return campaign

    def add_player(self, db: Session, campaign: Campaign, player_id: int):
        """
        Ajouter un joueur à une campagne.
        """
        if player_id not in [player.id for player in campaign.players]:
            campaign.players.append(player_id)
            db.commit()

    def remove_player(self, db: Session, campaign: Campaign, player_id: int):
        """
        Retirer un joueur d'une campagne.
        """
        campaign.players = [
            player for player in campaign.players if player.id != player_id
        ]
        db.commit()

    def add_npc(self, db: Session, campaign: Campaign, npc_id: int):
        """
        Ajouter un PNJ à une campagne.
        """
        if npc_id not in [npc.id for npc in campaign.npcs]:
            campaign.npcs.append(npc_id)
            db.commit()

    def remove_npc(self, db: Session, campaign: Campaign, npc_id: int):
        """
        Retirer un PNJ d'une campagne.
        """
        campaign.npcs = [npc for npc in campaign.npcs if npc.id != npc_id]
        db.commit()


# Initialisation de l'instance CRUDCampaign
crud_campaign = CRUDCampaign()
