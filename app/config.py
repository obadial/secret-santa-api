import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/database.db")
STAR_WARS_PLANETS = ["Tatooine", "Hoth", "Endor", "Naboo", "Coruscant", "Dagobah"]
DEFAULT_LIST_NAME = "Default Secret Santa List"
