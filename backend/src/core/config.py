import os

from dotenv import load_dotenv

from pydantic import BaseModel
load_dotenv()


class Settings(BaseModel):
    app_name: str = "Catalog Backend"
    debug: bool = True
    access_token_expire_minutes: int = 60 * 24


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")



settings = Settings()

