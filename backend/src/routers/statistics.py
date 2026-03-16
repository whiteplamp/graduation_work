from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.core.db import database
from src.models import Category, Product
from src.schemas import (
    AnalyticsCategoryItem,
    AnalyticsKpi,
    AnalyticsPoint,
    AnalyticsResponse,
    AnalyticsTopProduct,
)
import io
import csv

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(dateFrom: str, dateTo: str):
    # Для примера используем текущие остатки как суррогат продаж/выручки.
    with database.connection_context():
        total_revenue = 0.0
        total_costs = 0.0
        sold_count = 0

        for p in Product.select():
            total_revenue += float(p.price) * max(p.stock, 0)

        margin = 100.0 if total_revenue > 0 else 0.0

        kpi = AnalyticsKpi(
            revenue=round(total_revenue, 2),
            costs=round(total_costs, 2),
            soldCount=sold_count,
            margin=margin,
        )

        # Простейшая "динамика" — равномерно распределяем по датам
        start = datetime.fromisoformat(dateFrom)
        end = datetime.fromisoformat(dateTo)
        days = max((end - start).days, 1)
        sales_trend: List[AnalyticsPoint] = []
        for i in range(days + 1):
            day = start + timedelta(days=i)
            value = total_revenue / (days + 1) if total_revenue else 0
            sales_trend.append(AnalyticsPoint(date=day.date().isoformat(), value=round(value, 2)))

        # Структура по категориям
        by_category: List[AnalyticsCategoryItem] = []
        for cat in Category.select():
            cat_value = 0.0
            for p in cat.products:
                cat_value += float(p.price) * max(p.stock, 0)
            if cat_value:
                by_category.append(
                    AnalyticsCategoryItem(id=cat.id, name=cat.name, value=round(cat_value, 2))
                )

        # Топ товаров
        top_products: List[AnalyticsTopProduct] = []
        for p in Product.select().order_by(Product.stock.desc()).limit(10):
            revenue = float(p.price) * max(p.stock, 0)
            top_products.append(
                AnalyticsTopProduct(
                    productId=p.id,
                    name=p.name,
                    categoryName=p.category.name if p.category_id else None,
                    soldCount=p.stock,
                    revenue=round(revenue, 2),
                )
            )

        return AnalyticsResponse(
            kpi=kpi,
            salesTrend=sales_trend,
            salesByCategory=by_category,
            topProducts=top_products,
        )


@router.get("/export")
def export_report(dateFrom: str, dateTo: str):
    # Простой CSV-экспорт по товарам
    with database.connection_context():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "category", "price", "stock"])
        for p in Product.select():
            writer.writerow(
                [
                    p.id,
                    p.name,
                    p.category.name if p.category_id else "",
                    float(p.price),
                    p.stock,
                ]
            )
        csv_bytes = output.getvalue().encode("utf-8")
        output.close()

    filename = "analytics.csv"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(io.BytesIO(csv_bytes), media_type="text/csv", headers=headers)


