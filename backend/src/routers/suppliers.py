from fastapi import APIRouter, HTTPException

from src.core.db import database
from src.models import Supplier
from src.schemas import SupplierCreate, SupplierOut

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get("", response_model=dict)
def list_suppliers():
    with database.connection_context():
        items = [SupplierOut.model_validate(s) for s in Supplier.select().order_by(Supplier.name)]
        return {"items": items}


@router.post("", response_model=SupplierOut)
def create_supplier(data: SupplierCreate):
    with database.atomic():
        s = Supplier.create(**data.dict())
        return SupplierOut.model_validate(s)


@router.put("/{supplier_id}", response_model=SupplierOut)
def update_supplier(supplier_id: int, data: SupplierCreate):
    with database.atomic():
        try:
            s = Supplier.get_by_id(supplier_id)
        except Supplier.DoesNotExist:
            raise HTTPException(status_code=404, detail="Supplier not found")
        for field, value in data.dict().items():
            setattr(s, field, value)
        s.save()
        return SupplierOut.model_validate(s)


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int):
    with database.atomic():
        deleted = Supplier.delete().where(Supplier.id == supplier_id).execute()
        if not deleted:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return


