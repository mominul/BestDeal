from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

def collect_items(browser):
    results = []
    logo = './static/daraz.png'
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
        except Exception as e:
            if 'DEBUG' in os.environ:
                print(f"[Daraz search] Exception: {e}")
            pass

    return results

def scrape_daraz(query):
    options = Options()
    options.add_argument("--headless")
    # Cache browser data for faster scraping
    datadir = os.environ['HOME'] + "/BestDealData/Daraz"
    options.add_argument(f"user-data-dir={datadir}")
    options.binary_location = os.environ['BROWSER']
    browser = webdriver.Chrome(options=options)

    results = []
    
    encoded_query = query.replace(" ", "%20")

    browser.get(f'https://www.daraz.com.bd/catalog/?q={encoded_query}')

    # Scrape atleast first three pages
    for _ in range(0, 3):
        results += collect_items(browser)

        try:
            # Click on next page
            browser.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div/div/div[1]/div[3]/div/ul/li[9]/a').click()
        except:
            print("[Daraz] Error occured while finding the next button")
            break

    browser.quit()

    return results