from fastapi import APIRouter, Depends, HTTPException, Query
from peewee import fn

from src.core.db import database
from src.models import Category, Product, Supplier
from src.schemas import PaginatedProducts, ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=PaginatedProducts)
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    search: str | None = None,
    category_id: int | None = None,
    supplier_id: int | None = None,
    price_from: float | None = None,
    price_to: float | None = None,
    stock_from: int | None = None,
    stock_to: int | None = None,
):
    with database.connection_context():
        query = (
            Product.select(
                Product,
                Category.name.alias("category_name"),
                Supplier.name.alias("supplier_name"),
            )
            .join(Category, fn.LEFT_OUTER, on=(Product.category == Category.id))
            .switch(Product)
            .join(Supplier, fn.LEFT_OUTER, on=(Product.supplier == Supplier.id))
        )

        if search:
            query = query.where(
                (Product.name.contains(search)) | (Product.sku.contains(search))
            )
        if category_id:
            query = query.where(Product.category == category_id)
        if supplier_id:
            query = query.where(Product.supplier == supplier_id)
        if price_from is not None:
            query = query.where(Product.price >= price_from)
        if price_to is not None:
            query = query.where(Product.price <= price_to)
        if stock_from is not None:
            query = query.where(Product.stock >= stock_from)
        if stock_to is not None:
            query = query.where(Product.stock <= stock_to)

        total = query.count()
        items: list[ProductOut] = []
        for p in query.order_by(Product.id).paginate(page, page_size):
            items.append(
                ProductOut(
                    id=p.id,
                    sku=p.sku,
                    name=p.name,
                    category_id=p.category_id,
                    supplier_id=p.supplier_id,
                    price=float(p.price),
                    stock=p.stock,
                    category_name=getattr(p, "category_name", None),
                    supplier_name=getattr(p, "supplier_name", None),
                )
            )

        return PaginatedProducts(items=items, total=total)


@router.post("", response_model=ProductOut)
def create_product(data: ProductCreate):
    with database.atomic():
        if Product.select().where(Product.sku == data.sku).exists():
            raise HTTPException(
                status_code=400, detail="Product with this SKU already exists"
            )
        p = Product.create(
            sku=data.sku,
            name=data.name,
            category=data.category_id,
            supplier=data.supplier_id,
            price=data.price,
            stock=data.stock,
        )
        return ProductOut(
            id=p.id,
            sku=p.sku,
            name=p.name,
            category_id=p.category_id,
            supplier_id=p.supplier_id,
            price=float(p.price),
            stock=p.stock,
            category_name=p.category.name if p.category_id else None,
            supplier_name=p.supplier.name if p.supplier_id else None,
        )


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductCreate):
    with database.atomic():
        try:
            p = Product.get_by_id(product_id)
        except Product.DoesNotExist:
            raise HTTPException(status_code=404, detail="Product not found")

        p.sku = data.sku
        p.name = data.name
        p.category = data.category_id
        p.supplier = data.supplier_id
        p.price = data.price
        p.stock = data.stock
        p.save()

        return ProductOut(
            id=p.id,
            sku=p.sku,
            name=p.name,
            category_id=p.category_id,
            supplier_id=p.supplier_id,
            price=float(p.price),
            stock=p.stock,
            category_name=p.category.name if p.category_id else None,
            supplier_name=p.supplier.name if p.supplier_id else None,
        )


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    with database.atomic():
        deleted = Product.delete().where(Product.id == product_id).execute()
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        return


