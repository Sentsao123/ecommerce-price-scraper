import pandas as pd
from playwright.sync_api import sync_playwright
import time
import os
os.environ['DISPLAY'] = ':99'

def scrape_advice():
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
        page.goto("https://www.advice.co.th/product/smartphone", timeout=60000)
        page.wait_for_selector('div[code-product-item]')

        previous_height = 0
        scroll_pause_time = 10

        while True:
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(scroll_pause_time)

            products = page.query_selector_all('div[code-product-item]')
            current_count = len(products)

            if current_count == previous_height:
                break
            previous_height = current_count

        print(f'พบสินค้า {len(products)} รายการ')

        for product in products:
            try:
                name = product.get_attribute('item-name')
                link = product.query_selector('a').get_attribute('href')

                online_price_element = product.query_selector('.online-price .sales-price')
                online_price = online_price_element.inner_text().strip() if online_price_element else None
                price_int = int(''.join(filter(str.isdigit, online_price)))

                brand = name.split()[0] if name else None

                all_products.append({
                    'brand': brand,
                    'name': name,
                    'link': link,
                    'online_price': price_int,
                })

            except Exception as e:
                print(f"Error: {e}")

        browser.close()
        data=pd.DataFrame(all_products)
    return data

if __name__ == "__main__":
    df = scrape_advice()
    print(df)
