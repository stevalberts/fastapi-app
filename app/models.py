from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    sku = Column(String, unique=True, nullable=True)
    categories = Column(ARRAY(String), nullable=True)
    current_price = Column(String, nullable=True)
    original_price = Column(String, nullable=True)
    discount = Column(String, nullable=True)
    price_usd = Column(Float, nullable=True)
    discount_usd = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    rating = Column(String, nullable=True)
    reviews = Column(String, nullable=True)
    product_url = Column(String, unique=True, nullable=True)
    store_type = Column(String, nullable=True)
    campaign = Column(String, nullable=True)
    express_shipping = Column(Boolean, default=False)
    tags = Column(ARRAY(String), nullable=True)
    position = Column(String, nullable=True)
    page = Column(Integer, nullable=True)
    scraped_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # Use UTC timezone for scraped_at