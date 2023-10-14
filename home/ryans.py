from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

def scrape_ryans(query):
    # Initialize the Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    # Cache browser data for faster scraping
    datadir = os.environ['HOME'] + "/BestDealData/Ryans"
    options.add_argument(f"user-data-dir={datadir}")
    options.binary_location = os.environ['BROWSER']
    driver = webdriver.Chrome(options=options)

    # Encode the query for the URL
    encoded_query = query.replace(" ", "%20")

    # Send a request to the search page
    driver.get(f"https://www.ryanscomputers.com/search?q={encoded_query}")

    # Create a list to store search results
    search_results = []
    logo = './static/ryans.png'

    # Now, you can collect all the search results
    result_elements = driver.find_elements(By.XPATH, '//*[@id="search-box-html"]/div[4]/div/div/div')
    total_items = len(result_elements)

    for item_id in range(1, total_items):
        try:
            title = driver.find_element(By.XPATH, f'//*[@id="search-box-html"]/div[4]/div/div/div[{item_id}]/div[1]/div[2]/p[1]/a')
            price = driver.find_element(By.XPATH, f'//*[@id="search-box-html"]/div[4]/div/div/div[{item_id}]/div[1]/div[2]/p[3]')
            image = driver.find_element(By.XPATH, f'//*[@id="search-box-html"]/div[4]/div/div/div[{item_id}]/div[1]/div[1]/a/img').get_attribute('src')
            link = title.get_attribute('href')


            if (price.text == "Tk 0" ):
                continue

            search_results.append({
                "title": title.get_attribute('title'),
                "price": price.text,
                "image": image,
                "link": link,
                "logo": logo,
            })
        except Exception as e:
            if 'DEBUG' in os.environ:
                print(f"[Ryans search] Exception: {e}")
            pass

    # After scraping, close the browser window
    driver.quit()

    return search_results
