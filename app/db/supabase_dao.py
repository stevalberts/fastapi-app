from app.config import supabase
from app.schemas import ProductCreate, ProductResponse
from typing import List, Optional
from datetime import datetime

class ProductDAO:
    @staticmethod
    def create_product(product: ProductCreate) -> Optional[ProductResponse]:
        product_dict = product.model_dump()
        product_dict['scraped_at'] = product.scraped_at.isoformat() if product.scraped_at else None
        
        response = supabase.table('products').insert(product_dict).execute()
        return ProductResponse(**response.data[0]) if response.data else None

    @staticmethod
    def get_products(limit: int = 100, offset: int = 0) -> List[ProductResponse]:
        response = supabase.table('products').select("*").limit(limit).offset(offset).execute()
        return [ProductResponse(**product) for product in response.data]

    @staticmethod
    def get_product_by_sku(sku: str) -> Optional[ProductResponse]:
        response = supabase.table('products').select("*").eq('sku', sku).execute()
        return ProductResponse(**response.data[0]) if response.data else None

    @staticmethod
    def update_product(sku: str, product: ProductCreate) -> Optional[ProductResponse]:
        product_dict = product.model_dump()
        product_dict['scraped_at'] = product.scraped_at.isoformat() if product.scraped_at else None
        response = supabase.table('products').update(product_dict).eq('sku', sku).execute()
        return ProductResponse(**response.data[0]) if response.data else None

    @staticmethod
    def delete_product(sku: str) -> bool:
        response = supabase.table('products').delete().eq('sku', sku).execute()
        return bool(response.data)

    @staticmethod
    def get_products_by_page_range(start_page: int, end_page: int) -> List[ProductResponse]:
        response = supabase.table('products')\
            .select("*")\
            .gte('page', start_page)\
            .lte('page', end_page)\
            .execute()
        return [ProductResponse(**product) for product in response.data]