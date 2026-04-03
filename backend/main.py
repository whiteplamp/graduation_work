from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

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


@app.middleware("http")
async def log_errors_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        # Логируем ошибку с полной информацией о запросе
        print(f"\n🔴 ОШИБКА ПРИ ЗАПРОСЕ:")
        print(f"   Метод: {request.method}")
        print(f"   Путь: {request.url.path}")
        print(f"   Параметры: {dict(request.query_params)}")
        print(f"   Ошибка: {str(e)}")

        # Возвращаем ответ об ошибке
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


