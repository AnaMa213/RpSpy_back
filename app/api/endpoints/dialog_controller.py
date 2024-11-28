from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.crud_dialog import crud_dialog
from app.db.database import get_db
from app.schemas.schema_dialog import DialogCreate, DialogResponse, DialogUpdate
from app.utils.dependencies import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post(
    "/create", response_model=DialogResponse, status_code=status.HTTP_201_CREATED
)
def create_dialog(dialog_in: DialogCreate, db: Session = Depends(get_db)):
    """
    Créer un dialogue.
    """
    dialog = crud_dialog.create(db=db, obj_in=dialog_in)
    return dialog


@router.get("/{dialog_id}", response_model=DialogResponse)
def get_dialog(dialog_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un dialogue par son ID.
    """
    dialog = crud_dialog.get_by_id(db, dialog_id=dialog_id)
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")
    return dialog


@router.get("/session/{session_id}", response_model=List[DialogResponse])
def get_dialogs_by_session(session_id: int, db: Session = Depends(get_db)):
    """
    Récupérer tous les dialogues d'une session.
    """
    dialogs = crud_dialog.get_by_session(db, session_id=session_id)
    return dialogs


@router.put("/{dialog_id}/update", response_model=DialogResponse)
def update_dialog(
    dialog_id: int, dialog_in: DialogUpdate, db: Session = Depends(get_db)
):
    """
    Mettre à jour un dialogue par son ID.
    """
    db_dialog = crud_dialog.get_by_id(db, dialog_id=dialog_id)
    if not db_dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")
    updated_dialog = crud_dialog.update(db=db, db_obj=db_dialog, obj_in=dialog_in)
    return updated_dialog


@router.delete("/{dialog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dialog(dialog_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un dialogue par son ID.
    """
    dialog = crud_dialog.delete(db=db, dialog_id=dialog_id)
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")
    return {"detail": "Dialog deleted successfully"}
