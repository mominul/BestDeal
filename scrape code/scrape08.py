from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def scrape_and_save_search_results(query):
    # Initialize the Selenium WebDriver
    driver = webdriver.Firefox()

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
    for result_element in result_elements:
        result_text = result_element.text
        search_results.append(result_text)

    # After scraping, close the browser window
    driver.quit()

    # Filter out "Out of Stock" entries and remove "Add to Cart" string
    filtered_data = [entry.replace("Out of Stock", "").replace("Add to Cart", "").strip() for entry in search_results if "Out of Stock" not in entry]

    # Save the filtered search results to a JSON file
    with open(f'data/{query}_filtered_search_results.json', 'w', encoding='utf-8') as json_file:
        json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

    print(f"Filtered search results for '{query}' saved to {query}_filtered_search_results.json")

# Run the scraping task initially
user_query = input("Enter your search query: ")
scrape_and_save_search_results(user_query)
