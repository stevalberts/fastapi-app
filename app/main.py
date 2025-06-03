from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal, init_db
from app.models import Product
from app.schemas import PageRange, ProductResponse
from app.scraper import scrape_jumia

app = FastAPI(title="Jumia Uganda Catalog Scraper")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/scrape", response_model=List[ProductResponse])
async def scrape_products(page_range: PageRange, db: Session = Depends(get_db)):
    try:
        products = await scrape_jumia(page_range.start_page, page_range.end_page)

        for product_data in products:
            existing_product = db.query(Product).filter(Product.sku == product_data["sku"]).first()
            if not existing_product:
                db_product = Product(**product_data)
                db.add(db_product)
        db.commit()

        return db.query(Product).all()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product