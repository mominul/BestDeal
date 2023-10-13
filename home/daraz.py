from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os


def scrape_daraz(query):
    options = Options()
    options.add_argument("--headless") 
    # options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.binary_location = os.environ['BROWSER']
    browser = webdriver.Chrome(options=options)

    results = []
    logo = './static/daraz.png'

    for page in range(1, 2):
        encoded_query = query.replace(" ", "%20")

        browser.get(f'https://www.daraz.com.bd/catalog/?page={page}&q={encoded_query}')

        items = browser.find_elements(By.XPATH, '//div[starts-with(@data-qa-locator, "product-item")]')
        items = len(items)
        for item_id in range(1, items):
            try:
                title = browser.find_element(By.XPATH, f'//div[starts-with(@data-qa-locator, "product-item")][{item_id}]/div[1]/div/div[2]/div[2]/a')
                price = browser.find_element(By.XPATH, f'//div[starts-with(@data-qa-locator, "product-item")][{item_id}]/div[1]/div/div[2]/div[3]/span')
                image = browser.find_element(By.XPATH, f'//div[starts-with(@data-qa-locator, "product-item")][{item_id}]/div[1]/div/div[1]/div/a/img').get_attribute('src')
                link = title.get_attribute('href')
                results.append({
                    "title": title.text,
                    "price": price.text,
                    "image": image,
                    "link": link,
                    "logo" : logo,
                })
            except:
                pass


        browser.quit()

    return results