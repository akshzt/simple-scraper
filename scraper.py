import requests
from bs4 import BeautifulSoup
from storage import StorageInterface
from notifier import NotifierInterface
from cache import Cache
import os
from slugify import slugify
import uuid

class Scraper:
    def __init__(self, storage: StorageInterface, notifier: NotifierInterface, cache: Cache, settings):
        self.storage = storage
        self.notifier = notifier
        self.cache = cache
        self.settings = settings
        self.base_url = "https://dentalstall.com/shop/page/{}/"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        if self.settings.proxy:
            self.proxies = {"http": self.settings.proxy, "https": self.settings.proxy}
        else:
            self.proxies = None

    def run(self):
        page_limit = self.settings.page_limit or self.get_total_pages()
        scraped_count = 0

        for page_number in range(1, page_limit + 1):
            success = self.scrape_page(page_number)
            if not success:
                self.scrape_page(page_number)
            scraped_count += 1

        return scraped_count

    def scrape_page(self, page_number: int) -> bool:
        url = self.base_url.format(page_number)
        try:
            response = requests.get(url, headers=self.headers, proxies=self.proxies)
            print("response is", response.status_code, response.text)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('li', class_='product')
            data_to_store = []

            for product in products:
                title_tag = product.find('h2', class_='woo-loop-product__title')
                title = title_tag.get_text(strip=True) if title_tag else 'No title found'

                # Extract the price
                price_tag = product.find('span', class_='price')
                if price_tag:
                    # Check for a discounted price
                    ins_price = price_tag.find('ins')
                    if ins_price:
                        price = ins_price.get_text(strip=True)
                    else:
                        price = price_tag.get_text(strip=True)
                else:
                    price = 'No price found'

                # Extract the numerical price value
                price_extracted = None
                if price != 'No price found':
                    price = price.replace("Starting at:", "").strip()
                    rupee_pos = price.find('\u20b9')
                    if rupee_pos != -1:
                        price_extracted = price[rupee_pos + 1:]
                    else:
                        print(f"Rupee sign not found in price: {price}")

                image_container = product.find('div', class_='mf-product-thumbnail')
                if image_container:
                    img_tag = image_container.find('img')
                    if img_tag:
                        image_url = img_tag.get('data-lazy-src') or img_tag.get('src')
                    else:
                        image_url = 'No image URL found'
                else:
                    image_url = 'No image container found'

                # Save the image locally if image_url is available
                image_local = None
                if image_url and image_url != 'No image URL found' and image_url != 'No image container found':
                    try:
                        if not os.path.exists('images'):
                            os.makedirs('images')
                        
                        image_filename = f"{slugify(title[:50])}-{uuid.uuid4().hex[:8]}.jpg"
                        image_path = os.path.join('images', image_filename)
                        
                        img_response = requests.get(image_url)
                        img_response.raise_for_status()
                        with open(image_path, 'wb') as img_file:
                            img_file.write(img_response.content)
                        
                        image_local = image_path
                    except Exception as img_error:
                        print(f"Error saving image for {title}: {img_error}")

                cached_price = self.cache.get(title)
                if cached_price != price_extracted:
                    self.cache.set(title, price_extracted)
                    data_to_store.append({
                        "product_title": title,
                        "product_price": price,
                        "product_price_extracted": price_extracted,
                        "image_url": image_url,
                        "image_local": image_local,
                    })

            self.storage.save_data(data_to_store)
            return True
        except Exception as e:
            print(f"Error scraping page {page_number}: {e}")
            return False

    def get_total_pages(self):
        return 10
