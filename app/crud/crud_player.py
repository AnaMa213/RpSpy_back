from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.player import Player
from app.schemas.schema_player import PlayerCreate, PlayerUpdate


class CRUDPlayer:
    def get_by_id(self, db: Session, player_id: int) -> Optional[Player]:
        """
        Récupérer un joueur par son ID.
        """
        return db.query(Player).filter(Player.id == player_id).first()

    def get_by_user_id(self, db: Session, user_id: int) -> List[Player]:
        """
        Récupérer tous les joueurs d'un utilisateur spécifique.
        """
        return db.query(Player).filter(Player.user_id == user_id).all()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Player]:
        """
        Récupérer une liste de joueurs avec pagination.
        """
        return db.query(Player).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: PlayerCreate) -> Player:
        """
        Créer un nouveau joueur.
        """
        player = Player(
            name=obj_in.name,
            race=obj_in.race,
            class_name=obj_in.class_name,
            background=obj_in.background,
            alignment=obj_in.alignment,
            level=obj_in.level,
            strength=obj_in.strength,
            dexterity=obj_in.dexterity,
            constitution=obj_in.constitution,
            intelligence=obj_in.intelligence,
            wisdom=obj_in.wisdom,
            charisma=obj_in.charisma,
            current_hp=obj_in.current_hp,
            max_hp=obj_in.max_hp,
            skills=obj_in.skills,
            inventory=obj_in.inventory,
            description=obj_in.description,
            user_id=obj_in.user_id,
        )
        db.add(player)
        db.commit()
        db.refresh(player)
        return player

    def update(self, db: Session, db_obj: Player, obj_in: PlayerUpdate) -> Player:
        """
        Mettre à jour un joueur existant.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, player_id: int) -> Optional[Player]:
        """
        Supprimer un joueur par son ID.
        """
        player = db.query(Player).filter(Player.id == player_id).first()
        if player:
            db.delete(player)
            db.commit()
        return player

    def add_campaign(self, db: Session, player: Player, campaign_id: int):
        """
        Ajouter une campagne à un joueur.
        """
        if campaign_id not in [campaign.id for campaign in player.campaigns]:
            player.campaigns.append(campaign_id)
            db.commit()

    def remove_campaign(self, db: Session, player: Player, campaign_id: int):
        """
        Retirer une campagne d'un joueur.
        """
        player.campaigns = [
            campaign for campaign in player.campaigns if campaign.id != campaign_id
        ]
        db.commit()

    def add_session(self, db: Session, player: Player, session_id: int):
        """
        Ajouter une session à un joueur.
        """
        if session_id not in [session.id for session in player.sessions]:
            player.sessions.append(session_id)
            db.commit()

    def remove_session(self, db: Session, player: Player, session_id: int):
        """
        Retirer une session d'un joueur.
        """
        player.sessions = [
            session for session in player.sessions if session.id != session_id
        ]
        db.commit()


# Initialisation de l'instance CRUDPlayer
crud_player = CRUDPlayer()
