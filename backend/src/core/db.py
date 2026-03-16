from peewee import Model, PostgresqlDatabase

from src.core.config import DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASS

database = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
)


class BaseModel(Model):
    class Meta:
        database = database

