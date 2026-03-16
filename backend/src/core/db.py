from peewee import Model, PostgresqlDatabase

from src.core.config import settings


database = PostgresqlDatabase(
    settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
)


class BaseModel(Model):
    class Meta:
        database = database

