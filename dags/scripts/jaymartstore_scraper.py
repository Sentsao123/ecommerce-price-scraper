import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import re
import os
os.environ['DISPLAY'] = ':99'

def scrape_jaymartstore():
    all_products = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
        headless=False,
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--start-maximized"
        ]
    )
        context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )
        page = context.new_page()
        
        page.goto(f"https://jaymartstore.com/categories/1lx79X6TbkoYZx9ftBlurgMJChE", timeout=60000)

        page.wait_for_selector('div.product-item-container')

        previous_height = 0
        scroll_pause_time = 3

        while True:
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(scroll_pause_time)

            products = page.query_selector_all('div.product-item-container')
            current_count = len(products)

            if current_count == previous_height:
                break
            previous_height = current_count

        print(f'พบสินค้า {len(products)} รายการ')

        for product in products:
            try:
                link_element = product.query_selector('a.product-item')
                link = 'https://www.jaymartstore.com' + link_element.get_attribute('href')

                brand_element = product.query_selector('.brand span')
                brand = brand_element.inner_text().strip() if brand_element else None

                name_element = product.query_selector('.name span')
                name = name_element.inner_text().strip() if name_element else None

                price_element = product.query_selector('.price span')
                raw_price = price_element.inner_text().strip() if price_element else None
                price_numbers = re.findall(r'\d[\d,]*', raw_price)
                online_price = int(price_numbers[0].replace(',', '')) if price_numbers else None        

                all_products.append({
                    'brand': brand,
                    'name': name,
                    'link': link,
                    'online_price': online_price
                })

            except Exception as e:
                pass

        browser.close()
        data = pd.DataFrame(all_products)
    return data

if __name__ == "__main__":
    df = scrape_jaymartstore()
    print(df)
