from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time


def scrape_ryans(query):
    # Initialize the Selenium WebDriver
    options = Options()
    options.headless = True
    #options.binary_location = os.environ['BROWSER']
    driver = webdriver.Chrome(options=options)

    # Encode the query for the URL
    encoded_query = query.replace(" ", "%20")

    # Send a request to the search page
    driver.get(f"https://www.ryanscomputers.com/search?q={encoded_query}")

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-box-html"]/div[4]/div/div')))

    # Create a list to store search results
    search_results = []

    # Loop to keep clicking "Load More" until it's no longer available
    while True:
        try:
            load_more_button = driver.find_element(By.XPATH, '//*[@id="search-box-html"]/div[4]/div/div/div[21]/button')
            load_more_button.click()
            time.sleep(2)  # Wait for new results to load
        except Exception as e:
            break

    # Now, you can collect all the search results
    result_elements = driver.find_elements(By.XPATH, '//*[@id="search-box-html"]/div[4]/div/div/div')
    total_items = len(result_elements)

    for item_id in range(1, total_items):
        try:
            title = driver.find_element(By.XPATH, f'//*[@id="search-box-html"]/div[4]/div/div/div[{item_id}]/div[1]/div[2]/p[2]/a')
            price = driver.find_element(By.XPATH, f'//*[@id="search-box-html"]/div[4]/div/div/div[{item_id}]/div[1]/div[2]/p[3]')
            image = driver.find_element(By.XPATH, f'//*[@id="search-box-html"]/div[4]/div/div/div[{item_id}]/div[1]/div[1]/a/img').get_attribute('src')
            link = title.get_attribute('href')

            search_results.append({
                "title": title.text,
                "price": price.text,
                "image": image,
                "link": link,
            })
        except:
            pass

    # After scraping, close the browser window
    driver.quit()

    return search_results
