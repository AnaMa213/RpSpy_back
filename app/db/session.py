from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.models import Base

engine = create_engine(settings.POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fonction pour initialiser la base de données
def init_db():
    import app.db.models  # Assurez-vous que tous les modèles sont importés

    Base.metadata.create_all(bind=engine)
