import csv
from typing import List

from fastapi import APIRouter

from src.core.db import database
from src.core.debug import debug_error
from src.models import UploadJob, Supplier, Category, Product
from src.schemas import UploadStartResponse, UploadStatus, UploadPreview
import io
import pandas as pd
from fastapi import UploadFile, File, HTTPException
from decimal import Decimal
from peewee import DatabaseError

router = APIRouter(prefix="/upload", tags=["upload"])


COLUMN_MAPPING = {
    'артикул': 'sku',
    'sku': 'sku',
    'наименование': 'name',
    'name': 'name',
    'название': 'name',
    'категория': 'category',
    'category': 'category',
    'поставщик': 'supplier',
    'supplier': 'supplier',
    'цена': 'price',
    'price': 'price',
    'стоимость': 'price',
    'количество': 'stock',
    'stock': 'stock',
    'остаток': 'stock',
    'склад': 'stock'
}


def _build_preview_from_csv(file_bytes: bytes, limit: int = 10) -> UploadPreview:
    text = file_bytes.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    rows: list[dict] = []
    for idx, row in enumerate(reader):
        if idx >= limit:
            break
        rows.append(row)
    columns = list(reader.fieldnames or [])
    return UploadPreview(columns=columns, rows=rows)


async def upload_file_service(file: UploadFile = File(...)):
    """
    Загрузка файла с товарами.
    Поддерживаемые форматы: CSV, Excel (xlsx, xls)
    Поддерживаются русские и английские названия колонок
    """

    # Проверка расширения файла
    allowed_extensions = ['.csv', '.xlsx', '.xls']
    file_extension = '.' + file.filename.split('.')[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат файла. Разрешены: {', '.join(allowed_extensions)}"
        )

    # Чтение содержимого файла
    contents = await file.read()

    try:
        # Загрузка данных в зависимости от формата
        if file_extension == '.csv':
            df = pd.read_csv(io.BytesIO(contents))
        else:  # Excel файлы
            df = pd.read_excel(io.BytesIO(contents))

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка при чтении файла: {str(e)}"
        )

    # Маппинг колонок с русских на английские
    df.rename(columns=lambda x: COLUMN_MAPPING.get(x.lower().strip(), x), inplace=True)

    # Проверка наличия обязательных колонок (после маппинга)
    required_columns = ['sku', 'name']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}. "
                   f"Доступные колонки: {', '.join(df.columns)}. "
                   f"Поддерживаются русские названия: артикул, наименование, категория, поставщик, цена, количество"
        )

    # Обработка данных
    products_to_create = []
    errors = []
    categories_cache = {}
    suppliers_cache = {}

    # Информация о созданных категориях и поставщиках для ответа
    created_categories = set()
    created_suppliers = set()

    for index, row in df.iterrows():
        try:
            # Проверка обязательных полей
            if pd.isna(row['sku']) or pd.isna(row['name']):
                errors.append(f"Строка {index + 2}: артикул и наименование обязательны для заполнения")
                continue

            # Очистка и нормализация данных
            sku = str(row['sku']).strip()
            name = str(row['name']).strip()

            if not sku or not name:
                errors.append(f"Строка {index + 2}: артикул и наименование не могут быть пустыми")
                continue

            # Поиск или создание категории
            category_id = None
            if 'category' in df.columns and not pd.isna(row['category']):
                category_name = str(row['category']).strip()

                if category_name:  # Создаём категорию только если имя не пустое
                    if category_name in categories_cache:
                        category_id = categories_cache[category_name]
                    else:
                        # Ищем или создаём категорию
                        category, created = Category.get_or_create(
                            name=category_name,
                            defaults={'description': f'Автоматически создана из файла {file.filename}'}
                        )
                        category_id = category.id
                        categories_cache[category_name] = category_id

                        if created:
                            created_categories.add(category_name)

            # Поиск или создание поставщика
            supplier_id = None
            if 'supplier' in df.columns and not pd.isna(row['supplier']):
                supplier_name = str(row['supplier']).strip()

                if supplier_name:  # Создаём поставщика только если имя не пустое
                    if supplier_name in suppliers_cache:
                        supplier_id = suppliers_cache[supplier_name]
                    else:
                        # Ищем или создаём поставщика
                        supplier, created = Supplier.get_or_create(
                            name=supplier_name,
                            defaults={
                                'contact_person': None,
                                'phone': None,
                                'email': None,
                                'address': f'Автоматически создан из файла {file.filename}'
                            }
                        )
                        supplier_id = supplier.id
                        suppliers_cache[supplier_name] = supplier_id

                        if created:
                            created_suppliers.add(supplier_name)

            # Подготовка данных для товара
            price = Decimal('0')
            if 'price' in df.columns and not pd.isna(row['price']):
                try:
                    price = Decimal(str(row['price']).replace(',', '.'))
                    if price < 0:
                        raise ValueError("Цена не может быть отрицательной")
                except:
                    errors.append(f"Строка {index + 2}: некорректное значение цены '{row['price']}'")
                    continue

            stock = 0
            if 'stock' in df.columns and not pd.isna(row['stock']):
                try:
                    stock = int(float(row['stock']))  # На случай если пришло число с плавающей точкой
                    if stock < 0:
                        raise ValueError("Количество не может быть отрицательным")
                except:
                    errors.append(f"Строка {index + 2}: некорректное значение количества '{row['stock']}'")
                    continue

            product_data = {
                'sku': sku,
                'name': name,
                'category': category_id,
                'supplier': supplier_id,
                'price': price,
                'stock': stock
            }

            print(product_data)

            products_to_create.append(product_data)

        except Exception as e:
            errors.append(f"Строка {index + 2}: ошибка обработки - {str(e)}")

    if not products_to_create:
        error_msg = "Нет валидных данных для загрузки"
        if errors:
            error_msg += f". Ошибки: {', '.join(errors[:5])}"  # Показываем первые 5 ошибок
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )

    # Сохранение в базу данных
    created_count = 0
    updated_count = 0

    try:
        with database.atomic():
            for product_data in products_to_create:
                existing_product = Product.get_or_none(Product.sku == product_data['sku'])

                if existing_product:
                    # Обновление существующего товара
                    for key, value in product_data.items():
                        setattr(existing_product, key, value)
                    existing_product.save()
                    updated_count += 1
                else:
                    # Создание нового товара
                    Product.create(**product_data)
                    created_count += 1

    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка базы данных при сохранении: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при сохранении в базу данных: {str(e)}"
        )

    # Формирование информативного ответа
    message_parts = [
        f"Загружено товаров: создано {created_count}, обновлено {updated_count}",
        f"Всего строк в файле: {len(df)}",
        f"Ошибок: {len(errors)}"
    ]

    if created_categories:
        message_parts.append(
            f"🏷Создано категорий: {len(created_categories)} ({', '.join(list(created_categories)[:5])}{'...' if len(created_categories) > 5 else ''})")

    if created_suppliers:
        message_parts.append(
            f"Создано поставщиков: {len(created_suppliers)} ({', '.join(list(created_suppliers)[:5])}{'...' if len(created_suppliers) > 5 else ''})")

    return UploadStartResponse(
        success=True,
        total_rows=len(df),
        created=created_count,
        updated=updated_count,
        errors=errors if errors else None,
        message="\n".join(message_parts)
    )



@router.post("", response_model=UploadStartResponse)
@debug_error
async def upload_file(file: UploadFile = File(...)):
    return await upload_file_service(file)


@router.get("/{job_id}/status", response_model=UploadStatus)
def get_status(job_id: int):
    with database.connection_context():
        try:
            job = UploadJob.get_by_id(job_id)
        except UploadJob.DoesNotExist:
            raise HTTPException(status_code=404, detail="Job not found")

        return UploadStatus(
            progress=job.progress,
            processedRows=job.processed_rows,
            totalRows=job.total_rows,
            status=job.status,
            errorReportUrl=None,
        )


@router.post("/{job_id}/process", status_code=202)
def start_processing(job_id: int, body: dict):
    with database.atomic():
        try:
            job = UploadJob.get_by_id(job_id)
        except UploadJob.DoesNotExist:
            raise HTTPException(status_code=404, detail="Job not found")

        job.status = "completed"
        job.progress = 100
        if job.total_rows == 0:
            job.total_rows = job.processed_rows
        else:
            job.processed_rows = job.total_rows
        job.save()
    return {"status": "ok"}


@router.get("/{job_id}/errors")
def download_errors(job_id: int):
    from fastapi.responses import StreamingResponse

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["row", "error"])
    csv_bytes = output.getvalue().encode("utf-8")
    output.close()

    filename = f"errors_{job_id}.csv"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(io.BytesIO(csv_bytes), media_type="text/csv", headers=headers)


@router.get("/jobs/recent", response_model=List[dict])
def recent_jobs():
    with database.connection_context():
        items: list[dict] = []
        for job in UploadJob.select().order_by(UploadJob.created_at.desc()).limit(10):
            mode_labels = {
                "replace": "Замена каталога",
                "append": "Добавление",
                "update": "Обновление по артикулу",
            }
            status_labels = {
                "completed": "Завершена",
                "processing": "Обработка",
                "queued": "В очереди",
                "uploaded": "Загружен",
                "failed": "Ошибка",
            }
            items.append(
                {
                    "id": job.id,
                    "fileName": job.file_name,
                    "modeLabel": mode_labels.get(job.mode, job.mode),
                    "status": job.status,
                    "statusLabel": status_labels.get(job.status, job.status),
                    "successCount": job.processed_rows,
                    "errorCount": 0,
                    "createdAt": job.created_at,
                }
            )
        return items


