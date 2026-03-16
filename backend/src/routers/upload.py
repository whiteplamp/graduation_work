import csv
import io
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.core.db import database
from src.models import UploadJob
from src.schemas import UploadStartResponse, UploadStatus, UploadPreview

router = APIRouter(prefix="/upload", tags=["upload"])


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


@router.post("", response_model=UploadStartResponse)
async def upload_file(file: UploadFile = File(...), mode: str = File(...)):
    contents = await file.read()

    # Простая попытка сделать предпросмотр только для CSV
    preview = UploadPreview(columns=[], rows=[])
    if file.filename.lower().endswith(".csv"):
        preview = _build_preview_from_csv(contents)

    with database.atomic():
        job = UploadJob.create(
            file_name=file.filename,
            mode=mode,
            status="uploaded",
            progress=0,
            processed_rows=0,
            total_rows=len(preview.rows),
        )

    return UploadStartResponse(jobId=job.id, preview=preview)


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
    # В этой учебной версии просто отмечаем задачу как завершённую.
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
    # Пока всегда возвращаем пустой CSV, чтобы фронт мог скачать файл.
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


