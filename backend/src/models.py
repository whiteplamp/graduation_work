from datetime import datetime

from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    TextField,
)

from src.core.db import BaseModel


class User(BaseModel):
    id = AutoField()
    email = CharField(max_length=255, unique=True)
    name = CharField(max_length=255)
    hashed_password = CharField(max_length=255)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)


class Category(BaseModel):
    id = AutoField()
    name = CharField(max_length=255)
    parent = ForeignKeyField("self", null=True, backref="children", on_delete="SET NULL")


class Supplier(BaseModel):
    id = AutoField()
    name = CharField(max_length=255)
    email = CharField(max_length=255, null=True)
    phone = CharField(max_length=50, null=True)
    website = CharField(max_length=255, null=True)
    note = TextField(null=True)


class Product(BaseModel):
    id = AutoField()
    sku = CharField(max_length=100, unique=True)
    name = CharField(max_length=255)
    category = ForeignKeyField(Category, null=True, backref="products", on_delete="SET NULL")
    supplier = ForeignKeyField(Supplier, null=True, backref="products", on_delete="SET NULL")
    price = DecimalField(max_digits=12, decimal_places=2, default=0)
    stock = IntegerField(default=0)


class UploadJob(BaseModel):
    id = AutoField()
    file_name = CharField(max_length=255)
    mode = CharField(max_length=50)  # replace / append / update
    status = CharField(max_length=50, default="queued")
    progress = IntegerField(default=0)
    processed_rows = IntegerField(default=0)
    total_rows = IntegerField(default=0)
    error_report_path = CharField(max_length=255, null=True)
    created_at = DateTimeField(default=datetime.utcnow)


class MappingTemplate(BaseModel):
    id = AutoField()
    name = CharField(max_length=255)
    mapping_json = TextField()
    created_at = DateTimeField(default=datetime.utcnow)


class ImportSettings(BaseModel):
    id = AutoField()
    date_format = CharField(max_length=50, default="dd.MM.yyyy")
    csv_delimiter = CharField(max_length=10, default=";")
    currency = CharField(max_length=10, default="RUB")


