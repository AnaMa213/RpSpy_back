from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_npc
from app.db.database import get_db
from app.schemas.schema_npc import NPCCreate, NPCResponse, NPCUpdate
from app.utils.dependencies import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post("/create", response_model=NPCResponse, status_code=status.HTTP_201_CREATED)
def create_npc(npc_data: NPCCreate, db: Session = Depends(get_db)):
    # Créer un nouveau PNJ
    npc = crud_npc.create(db=db, obj_in=npc_data)
    return npc


@router.put("/{npc_id}", response_model=NPCResponse)
def update_npc(npc_id: int, npc_update: NPCUpdate, db: Session = Depends(get_db)):
    # Récupérer le PNJ
    db_npc = crud_npc.get_by_id(db, npc_id=npc_id)
    if not db_npc:
        raise HTTPException(status_code=404, detail="PNJ non trouvé")
    updated_npc = crud_npc.update(db=db, db_obj=db_npc, obj_in=npc_update)
    return updated_npc


@router.delete("/{npc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_npc(npc_id: int, db: Session = Depends(get_db)):
    npc = crud_npc.delete(db=db, npc_id=npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="PNJ non trouvé")
    return {"detail": "PNJ supprimé avec succès"}
