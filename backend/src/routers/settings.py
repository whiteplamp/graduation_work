from fastapi import APIRouter

from src.core.db import database
from src.models import ImportSettings
from src.schemas import ImportSettingsOut, ImportSettingsUpdate

router = APIRouter(prefix="/settings", tags=["settings"])


def _get_single_settings() -> ImportSettings:
    settings_obj, _ = ImportSettings.get_or_create(id=1)
    return settings_obj


@router.get("/import", response_model=ImportSettingsOut)
def get_import_settings():
    with database.connection_context():
        s = _get_single_settings()
        return ImportSettingsOut(
            dateFormat=s.date_format,
            csvDelimiter=s.csv_delimiter,
            currency=s.currency,
        )


@router.put("/import", response_model=ImportSettingsOut)
def update_import_settings(data: ImportSettingsUpdate):
    with database.atomic():
        s = _get_single_settings()
        s.date_format = data.dateFormat
        s.csv_delimiter = data.csvDelimiter
        s.currency = data.currency
        s.save()
        return ImportSettingsOut(
            dateFormat=s.date_format,
            csvDelimiter=s.csv_delimiter,
            currency=s.currency,
        )


