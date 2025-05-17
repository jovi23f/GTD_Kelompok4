from databases import Database
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ro_user:ro_password@localhost:5432/terrorism_db")

database = Database(DATABASE_URL)