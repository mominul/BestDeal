from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

def scrape_pickaboo(query):
    # Initialize the Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    # Cache browser data for faster scraping
    datadir = os.environ['HOME'] + "/BestDealData/Pickaboo"
    options.add_argument(f"user-data-dir={datadir}")
    options.binary_location = os.environ['BROWSER']
    driver = webdriver.Chrome(options=options)

    # Encode the query for the URL
    encoded_query = query.replace(" ", "%20")

    # Send a request to the search page
    driver.get(f"https://www.pickaboo.com/search-result/{encoded_query}")
    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section/div[2]/div/div[2]/div[2]/div')))
    # Create a list to store search results
    search_results = []
    logo = './static/pickaboo.png'

    # Now, you can collect all the search results
    result_elements = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/section/div[2]/div/div[2]/div[2]/div')
    
    total_items = len(result_elements)

    for item_id in range(1, total_items):
        try:

            title = driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/div[2]/div/div[2]/div[2]/div[{item_id}]/div/a/div/div/div[2]/h4')
            price = driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/div[2]/div/div[2]/div[2]/div[{item_id}]/div/a/div/div/div[2]/p/span')
            image = driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/div[2]/div/div[2]/div[2]/div[{item_id}]/div/a/div/div/div[1]/img').get_attribute('src')
            link = title.get_attribute('href')
            query_set = set(query.lower().split())
            title_set = set(title.text.lower().split())
            if not query_set.issubset(title_set):
                raise Exception("Query doesn't match")
            search_results.append({
                "title": title.text,
                "price": price.text,
                "image": image,
                "link": link,
                "logo": logo,
            })
        except Exception as e:
            if 'DEBUG' in os.environ:
                print(f"[Pickaboo search] Exception: {e}")
            pass

    # After scraping, close the browser window
    driver.quit()

    return search_results
