import json
from typing import List

from fastapi import APIRouter, HTTPException

from src.core.db import database
from src.models import MappingTemplate
from src.schemas import MappingTemplateIn, MappingTemplateOut

router = APIRouter(prefix="/mapping-templates", tags=["mapping-templates"])


@router.get("", response_model=List[MappingTemplateOut])
def list_templates():
    with database.connection_context():
        items: list[MappingTemplateOut] = []
        for tpl in MappingTemplate.select().order_by(MappingTemplate.created_at.desc()):
            items.append(
                MappingTemplateOut(
                    id=tpl.id,
                    name=tpl.name,
                    mapping=json.loads(tpl.mapping_json),
                    createdAt=tpl.created_at,
                )
            )
        return items


@router.post("", response_model=MappingTemplateOut)
def create_template(body: MappingTemplateIn):
    with database.atomic():
        tpl = MappingTemplate.create(
            name=body.name,
            mapping_json=json.dumps(body.mapping, ensure_ascii=False),
        )
        return MappingTemplateOut(
            id=tpl.id,
            name=tpl.name,
            mapping=body.mapping,
            createdAt=tpl.created_at,
        )


@router.delete("/{template_id}", status_code=204)
def delete_template(template_id: int):
    with database.atomic():
        deleted = MappingTemplate.delete().where(MappingTemplate.id == template_id).execute()
        if not deleted:
            raise HTTPException(status_code=404, detail="Template not found")
        return


