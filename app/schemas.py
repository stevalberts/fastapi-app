from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PageRange(BaseModel):
    start_page: int
    end_page: int

class ProductCreate(BaseModel):
    name: str
    brand: Optional[str] = None
    sku: Optional[str] = None
    categories: List[Optional[str]] = None
    current_price: Optional[str] = None
    original_price: Optional[str] = None
    discount: Optional[str] = None
    price_usd: Optional[float] = None
    discount_usd: Optional[float] = None
    image_url: Optional[str] = None
    rating: Optional[str] = None
    reviews: Optional[str] = None
    product_url: Optional[str] = None
    store_type: Optional[str] = None
    campaign: Optional[str] = None
    express_shipping: bool = False
    tags: Optional[List[str]] = None
    position: Optional[str] = None
    page: Optional[int] = None
    scraped_at: Optional[datetime] = None

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True