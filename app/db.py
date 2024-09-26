from sqlmodel import SQLModel, create_engine
from app.config import DATABASE_URL
import os

# Création de l'instance d'engine
engine = create_engine(DATABASE_URL, echo=True)

# Fonction pour créer la base de données et les tables si elles n'existent pas
def create_db_and_tables():
    if not os.path.exists("./data"):
        os.makedirs("./data")  # Crée le répertoire data s'il n'existe pas

    SQLModel.metadata.create_all(engine)
