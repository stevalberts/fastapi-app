from fastapi import FastAPI, HTTPException
from typing import List
from app.schemas import PageRange, ProductResponse, ProductCreate
from app.scraper import scrape_jumia
from app.db.supabase_dao import ProductDAO

app = FastAPI(title="Jumia Uganda Catalog Scraper")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Jumia Uganda Catalog Scraper API"}

@app.post("/scrape", response_model=List[ProductResponse])
async def scrape_products(page_range: PageRange):
    try:
        products = await scrape_jumia(page_range.start_page, page_range.end_page)

        saved_products = []
        for product_data in products:
            # Check if product exists
            existing_product = ProductDAO.get_product_by_sku(product_data["sku"])
            if not existing_product:
                # Create new product
                product = ProductCreate(**product_data)
                saved_product = ProductDAO.create_product(product)
                if saved_product:
                    saved_products.append(saved_product)

        return saved_products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/products", response_model=List[ProductResponse])
async def get_products(limit: int = 100, offset: int = 0):
    return ProductDAO.get_products(limit=limit, offset=offset)

@app.get("/products/{sku}", response_model=ProductResponse)
async def get_product(sku: str):
    product = ProductDAO.get_product_by_sku(sku)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{sku}")
async def delete_product(sku: str):
    deleted = ProductDAO.delete_product(sku)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}