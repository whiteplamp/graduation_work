from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import database
from src.models import (
    Category,
    ImportSettings,
    MappingTemplate,
    Product,
    Supplier,
    UploadJob,
    User,
)
from src.routers import (
    auth,
    products,
    categories,
    suppliers,
    settings,
    profile,
    dashboard,
    upload,
    statistics,
    mapping_templates,
)


app = FastAPI(title="Catalog Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.create_tables(
    [User, Category, Supplier, Product, UploadJob, MappingTemplate, ImportSettings]
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(dashboard.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(suppliers.router)
app.include_router(upload.router)
app.include_router(statistics.router)
app.include_router(mapping_templates.router)
app.include_router(settings.router)

@app.get("/health")
def health():
    return {"status": "ok"}


