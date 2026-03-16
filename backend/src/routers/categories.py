from fastapi import APIRouter, HTTPException

from src.core.db import database
from src.models import Category
from src.schemas import CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


def build_tree(nodes: list[Category]) -> list[CategoryOut]:
    by_id: dict[int, CategoryOut] = {}
    roots: list[CategoryOut] = []

    for n in nodes:
        by_id[n.id] = CategoryOut(id=n.id, name=n.name, parent_id=n.parent_id, children=[])

    for n in nodes:
        node = by_id[n.id]
        if n.parent_id and n.parent_id in by_id:
            by_id[n.parent_id].children.append(node)  # type: ignore[union-attr]
        else:
            roots.append(node)

    return roots


@router.get("/tree", response_model=list[CategoryOut])
def get_tree():
    with database.connection_context():
        nodes = list(Category.select().order_by(Category.id))
        return build_tree(nodes)


@router.get("/flat", response_model=list[CategoryOut])
def get_flat():
    with database.connection_context():
        return [CategoryOut.model_validate(c) for c in Category.select().order_by(Category.name)]


@router.post("", response_model=CategoryOut)
def create_category(name: str, parent_id: int | None = None):
    with database.atomic():
        c = Category.create(name=name, parent=parent_id)
        return CategoryOut.model_validate(c)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, name: str, parent_id: int | None = None):
    with database.atomic():
        try:
            c = Category.get_by_id(category_id)
        except Category.DoesNotExist:
            raise HTTPException(status_code=404, detail="Category not found")
        c.name = name
        c.parent = parent_id
        c.save()
        return CategoryOut.model_validate(c)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int):
    with database.atomic():
        deleted = Category.delete().where(Category.id == category_id).execute()
        if not deleted:
            raise HTTPException(status_code=404, detail="Category not found")
        return


