from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_campaign
from app.db.database import get_db
from app.schemas.schema_campaign import CampaignCreate, CampaignResponse, CampaignUpdate
from app.utils.dependencies import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post(
    "/create", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED
)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    # Créer une nouvelle campagne
    campaign = crud_campaign.create(db=db, obj_in=campaign)
    return campaign


@router.put("/{campaign_id}/update", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int, campaign_update: CampaignUpdate, db: Session = Depends(get_db)
):
    # Récupérer la campagne
    """
    Mettre à jour une campagne

    Args:
        campaign_id (int): ID de la campagne
        campaign_update (CampaignUpdate): Informations de la campagne à mettre à jour

    Raises:
        HTTPException: Si la campagne n'est pas trouvée ou si vous n'êtes pas le propriétaire
    """
    db_campaign = crud_campaign.get_by_id(db, campaign_id=campaign_id)
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")
    updated_campaign = crud_campaign.update(
        db=db, db_obj=db_campaign, obj_in=campaign_update
    )
    return updated_campaign


@router.delete("/{campaign_id}/remove", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    # Récupérer la campagne
    """
    Supprimer une campagne

    Args:
        campaign_id (int): ID de la campagne

    Raises:
        HTTPException: Si la campagne n'est pas trouvée ou si vous n'êtes pas le propriétaire
    """
    campaign = crud_campaign.delete(db=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")
    return {"detail": "Campagne supprimée avec succès"}
