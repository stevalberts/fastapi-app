import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timezone

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.jumia.ug/"
}

base_url = "https://www.jumia.ug/catalog/"

async def scrape_jumia(start_page: int, end_page: int):
    product_list = []

    for page in range(start_page, end_page + 1):
        url = f"{base_url}?page={page}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("article", class_="prd _fb col c-prd")

        if not products:
            print(f"No products found on page {page}. Stopping.")
            break

         # Loop through each product article
        for product in products:
            product_data = {}

            # Extract product information
            product_data["name"] = product.find("h3", class_="name").text.strip() if product.find("h3", class_="name") else None
            core_link = product.find("a", class_="core")
            product_data["brand"] = core_link.get("data-ga4-item_brand") if core_link and core_link.get("data-ga4-item_brand") else None
            product_data["sku"] = core_link.get("data-sku") or core_link.get("data-gtm-id") or core_link.get("data-ga4-item_id") if core_link else None
            product_data["categories"] = [
                core_link.get("data-ga4-item_category", None) if core_link else None,
                core_link.get("data-ga4-item_category2", None) if core_link else None,
                core_link.get("data-ga4-item_category3", None) if core_link else None,
                core_link.get("data-ga4-item_category4", None) if core_link else None
            ]

            # Extract pricing details
            product_data["current_price"] = product.find("div", class_="prc").text.strip() if product.find("div", class_="prc") else None
            product_data["original_price"] = product.find("div", class_="old").text.strip() if product.find("div", class_="old") else None
            product_data["discount"] = product.find("div", class_="bdg _dsct _sm").text.strip() if product.find("div", class_="bdg _dsct _sm") else None
            product_data["price_usd"] = core_link.get("data-gtm-price", None) if core_link else None
            product_data["discount_usd"] = core_link.get("data-ga4-discount", None) if core_link else None

            # Extract product image
            img_tag = product.find("img", class_="img")
            product_data["image_url"] = img_tag.get("data-src") if img_tag and img_tag.get("data-src") else None

            # Extract product rating
            rating_div = product.find("div", class_="stars _s")
            product_data["rating"] = rating_div.text.strip().split(" out of ")[0] if rating_div else None
            rev_div = product.find("div", class_="rev")
            product_data["reviews"] = rev_div.text.strip().split("(")[-1].replace(")", "") if rev_div and "(" in rev_div.text else None

            # Extract product URL
            product_data["product_url"] = f"https://www.jumia.ug{core_link.get('href')}" if core_link and core_link.get("href") else None

            # Extract badges and labels
            product_data["store_type"] = product.find("div", class_="bdg _mall _xs").text.strip() if product.find("div", class_="bdg _mall _xs") else None
            product_data["campaign"] = product.find("span", class_="bdg _xs camp").text.strip() if product.find("span", class_="bdg _xs camp") else None
            product_data["express_shipping"] = bool(product.find("svg", {"aria-label": "Express Shipping"}))

            # Extract tags and position
            product_data["tags"] = core_link.get("data-ga4-tags", "").split("|")[:5] if core_link and core_link.get("data-ga4-tags") else []
            product_data["position"] = core_link.get("data-ga4-index", None) if core_link else None
            product_data["page"] = page
            product_data["scraped_at"] = datetime.now(timezone.utc)

            # Append to product list
            product_list.append(product_data)

        # Add a delay to avoid overwhelming the server
        time.sleep(1)


    return product_list