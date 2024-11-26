from sqlalchemy.ext.declarative import declarative_base

# Importez tous vos modèles ici

Base = declarative_base()


# Importez vos modèles ici pour qu'Alembic les détecte
def import_models():
    from app.db.models.user import User  # Import différé
