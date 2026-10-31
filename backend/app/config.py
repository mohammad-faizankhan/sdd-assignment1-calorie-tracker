import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = Path(os.getenv("NUTRITION_DB_PATH", str(DATA_DIR / "tracker.db")))
