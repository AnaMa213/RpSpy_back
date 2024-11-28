from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_player
from app.db.database import get_db
from app.schemas.schema_player import PlayerCreate, PlayerResponse, PlayerUpdate
from app.utils.dependencies import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post(
    "/create", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED
)
def create_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    # Créer un nouveau joueur
    """
    Crée un nouveau personnage

    Args:
        player_data (PlayerCreate): Les informations du personnage à créer
        db (Session): La session de la base de données
        current_user (dict): Les informations de l'utilisateur actuel

    Returns:
        PlayerResponse: Le personnage créé

    Raises:
        HTTPException: Si le personnage n'est pas créé (par exemple, si le nom est déjà pris)
    """
    player = crud_player.create(db=db, obj_in=player_data)
    return player


@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(
    player_id: int, player_update: PlayerUpdate, db: Session = Depends(get_db)
):
    # Récupérer le joueur
    """
    Mettre à jour un personnage

    Args:
        player_id (int): Identifiant du personnage
        player_update (PlayerUpdate): Informations du personnage à mettre à jour

    Raises:
        HTTPException: Si le personnage n'est pas trouvé
    """
    db_player = crud_player.get_by_id(db, player_id=player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    updated_player = crud_player.update(db=db, db_obj=db_player, obj_in=player_update)
    return updated_player


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    # Récupérer le joueur
    """
    Supprimer un personnage

    Args:
        player_id (int): Identifiant du personnage

    Raises:
        HTTPException: Si le personnage n'est pas trouvé ou si vous n'êtes pas le propriétaire
    """
    player = crud_player.delete(db=db, player_id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    return {"detail": "Joueur supprimé avec succès"}
