import cloudinary.uploader
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session as DBSession

from app.crud import crud_session
from app.db.database import get_db
from app.db.models.campaign_session import CampaignSession
from app.schemas.schema_session import SessionCreate, SessionResponse, SessionUpdate
from app.utils.dependencies import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post(
    "/create", response_model=SessionResponse, status_code=status.HTTP_201_CREATED
)
def create_session(session_data: SessionCreate, db: CampaignSession = Depends(get_db)):
    # Vérifier si la campagne existe et appartient à l'utilisateur
    """
    Create a new session within a specific campaign.

    This endpoint creates a new session for a given campaign, ensuring
    that the campaign exists and belongs to the current user before
    proceeding with the session creation.

    Args:
        campaign_id (int): The ID of the campaign to which the session belongs.
        session_data (SessionCreate): The details of the session to be created.
        db (Session): The database session used for adding the new session.
        current_user (dict): The current user details obtained via the token.

    Returns:
        SessionResponse: The newly created session object.

    Raises:
        HTTPException: If the campaign is not found or if the user does not own the campaign.
    """
    session = crud_session.create(db=db, obj_in=session_data)
    return session


@router.put("/{session_id}", response_model=SessionResponse)
def update_session(
    session_id: int,
    session_update: SessionUpdate,
    db: CampaignSession = Depends(get_db),
):
    # Vérifier si la session existe et appartient à l'utilisateur
    """
    Mettre à jour une session

    Args:
        session_id (int): L'identifiant de la session à mettre à jour.
        session_update (SessionUpdate): Les informations de la session à mettre à jour.

    Raises:
        HTTPException: Si la session n'est pas trouvée ou si vous n'êtes pas le propriétaire
            de la session.
    """
    db_session = crud_session.get_by_id(db, session_id=session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    updated_session = crud_session.update(
        db=db, db_obj=db_session, obj_in=session_update
    )
    return updated_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: CampaignSession = Depends(get_db)):
    # Vérifier si la session existe et appartient à l'utilisateur
    """
    Supprimer une session

    Cette fonction supprime une session spécifique de la base de données si elle
    existe et appartient à l'utilisateur actuel. Elle vérifie l'existence de la
    session et la propriété avant de procéder à la suppression.

    Args:
        session_id (int): L'identifiant de la session à supprimer.
        db (Session): La session de base de données utilisée pour interagir avec les
            enregistrements de session.
        current_user (dict): Les détails de l'utilisateur actuel obtenus via le token de
            vérification.

    Raises:
        HTTPException: Si la session n'est pas trouvée ou si l'utilisateur actuel n'est
            pas le propriétaire de la session.
    """
    session = crud_session.delete(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    return {"detail": "Session supprimée avec succès"}


@router.post("/{session_id}/upload-audio")
async def upload_audio_to_cloudinary(
    session_id: int, file: UploadFile = File(...), db: DBSession = Depends(get_db)
):
    """
    Upload an audio file to Cloudinary for a given session.

    Args:
        session_id (int): The ID of the session.
        file (UploadFile): The audio file to upload.

    Raises:
        HTTPException: If the session does not exist or if the file is not an audio.

    Returns:
        dict: A JSON response with a message and the URL of the uploaded audio.
    """
    # Vérifiez si la session existe
    session = db.query(CampaignSession).filter(CampaignSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Vérifiez que le fichier est un audio
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio")

    # Upload du fichier sur Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(
            file.file,
            resource_type="video",  # Les fichiers audio sont traités comme des vidéos par Cloudinary
            folder=f"sessions/{session_id}",
            public_id=file.filename.split(".")[0],  # Nom du fichier sans extension
            overwrite=True,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Cloudinary upload failed: {e}"
        ) from e

    # Mise à jour de la session avec l'URL de l'audio
    session.audio_path = upload_result.get("secure_url")
    db.commit()
    db.refresh(session)

    return {"message": "Audio uploaded successfully", "audio_url": session.audio_path}
