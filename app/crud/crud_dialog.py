from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.dialog import Dialog
from app.schemas.schema_dialog import DialogCreate, DialogUpdate


class CRUDDialog:
    def get_by_id(self, db: Session, dialog_id: int) -> Optional[Dialog]:
        """
        Récupérer un dialogue par son ID.
        """
        return db.query(Dialog).filter(Dialog.id == dialog_id).first()

    def get_by_session(self, db: Session, session_id: int) -> List[Dialog]:
        """
        Récupérer tous les dialogues liés à une session spécifique.
        """
        return db.query(Dialog).filter(Dialog.session_id == session_id).all()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Dialog]:
        """
        Récupérer plusieurs dialogues avec pagination.
        """
        return db.query(Dialog).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: DialogCreate) -> Dialog:
        """
        Créer un nouveau dialogue.
        """
        dialog = Dialog(
            order=obj_in.order,
            start=obj_in.start,
            end=obj_in.end,
            speaker_id=obj_in.speaker_id,
            speaker=obj_in.speaker,
            content=obj_in.content,
            session_id=obj_in.session_id,
        )
        db.add(dialog)
        db.commit()
        db.refresh(dialog)
        return dialog

    def update(self, db: Session, db_obj: Dialog, obj_in: DialogUpdate) -> Dialog:
        """
        Mettre à jour un dialogue existant.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, dialog_id: int) -> Optional[Dialog]:
        """
        Supprimer un dialogue par son ID.
        """
        dialog = db.query(Dialog).filter(Dialog.id == dialog_id).first()
        if dialog:
            db.delete(dialog)
            db.commit()
        return dialog


# Instance CRUDDialog
crud_dialog = CRUDDialog()
