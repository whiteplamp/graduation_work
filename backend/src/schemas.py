from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    token: str
    user: UserOut


class LoginRequest(BaseModel):
    login: str
    password: str


class CategoryOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    children: Optional[List["CategoryOut"]] = None

    class Config:
        from_attributes = True


CategoryOut.model_rebuild()


class SupplierBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    note: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierOut(SupplierBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    sku: str
    name: str
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    price: float = 0
    stock: int = 0


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    category_name: Optional[str] = None
    supplier_name: Optional[str] = None

    class Config:
        from_attributes = True


class PaginatedProducts(BaseModel):
    items: List[ProductOut]
    total: int


class UploadPreview(BaseModel):
    columns: list[str]
    rows: list[dict]


class UploadStartResponse(BaseModel):
    success: bool
    total_rows: int
    created: int
    updated: int
    errors: Optional[List[str]] = None
    message: str


class UploadStatus(BaseModel):
    progress: int
    processedRows: int
    totalRows: int
    status: str
    errorReportUrl: Optional[str] = None


class MappingTemplateIn(BaseModel):
    name: str
    mapping: dict


class MappingTemplateOut(BaseModel):
    id: int
    name: str
    mapping: dict
    createdAt: datetime

    class Config:
        from_attributes = True


class ImportSettingsOut(BaseModel):
    dateFormat: str
    csvDelimiter: str
    currency: str


class ImportSettingsUpdate(BaseModel):
    dateFormat: str
    csvDelimiter: str
    currency: str


class DashboardStats(BaseModel):
    totalProducts: int
    totalSuppliers: int
    totalCategories: int
    productsWithoutCategory: int
    productsWithoutSupplier: int
    failedUploads: int


class DashboardUploadItem(BaseModel):
    id: int
    name: str
    modeLabel: str
    status: str
    statusLabel: str
    createdAt: datetime


class DashboardOverview(BaseModel):
    stats: DashboardStats
    recentUploads: List[DashboardUploadItem]


class AnalyticsKpi(BaseModel):
    revenue: float
    costs: float
    soldCount: int
    margin: float


class AnalyticsPoint(BaseModel):
    date: str
    value: float


class AnalyticsCategoryItem(BaseModel):
    id: int
    name: str
    value: float


class AnalyticsTopProduct(BaseModel):
    productId: int
    name: str
    categoryName: Optional[str] = None
    soldCount: int
    revenue: float


class AnalyticsResponse(BaseModel):
    kpi: AnalyticsKpi
    salesTrend: List[AnalyticsPoint]
    salesByCategory: List[AnalyticsCategoryItem]
    topProducts: List[AnalyticsTopProduct]


class ProfileUpdate(BaseModel):
    name: str
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str
    newPasswordConfirmation: str


