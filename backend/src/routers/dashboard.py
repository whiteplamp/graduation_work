from fastapi import APIRouter
from peewee import fn

from src.core.db import database
from src.models import Category, Product, Supplier, UploadJob
from src.schemas import DashboardOverview, DashboardStats, DashboardUploadItem

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
def get_overview():
    with database.connection_context():
        total_products = Product.select().count()
        total_suppliers = Supplier.select().count()
        total_categories = Category.select().count()
        products_without_category = Product.select().where(Product.category.is_null()).count()
        products_without_supplier = Product.select().where(Product.supplier.is_null()).count()
        failed_uploads = UploadJob.select().where(UploadJob.status == "failed").count()

        stats = DashboardStats(
            totalProducts=total_products,
            totalSuppliers=total_suppliers,
            totalCategories=total_categories,
            productsWithoutCategory=products_without_category,
            productsWithoutSupplier=products_without_supplier,
            failedUploads=failed_uploads,
        )

        recent: list[DashboardUploadItem] = []
        for job in (
            UploadJob.select().order_by(UploadJob.created_at.desc()).limit(5)
        ):
            mode_labels = {
                "replace": "Замена каталога",
                "append": "Добавление",
                "update": "Обновление по артикулу",
            }
            status_labels = {
                "completed": "Завершена",
                "processing": "Обработка",
                "queued": "В очереди",
                "failed": "Ошибка",
            }
            recent.append(
                DashboardUploadItem(
                    id=job.id,
                    name=job.file_name,
                    modeLabel=mode_labels.get(job.mode, job.mode),
                    status=job.status,
                    statusLabel=status_labels.get(job.status, job.status),
                    createdAt=job.created_at,
                )
            )

        return DashboardOverview(stats=stats, recentUploads=recent)


