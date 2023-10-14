# BestDeal
A Comparative Shopping Web Application


BestDeal is a powerful Comparative Shopping Web Application that empowers users to find the best prices for products across various online platforms. With a user-friendly interface and robust web scraping capabilities, BestDeal simplifies the process of comparing prices, making informed purchasing decisions, and saving money. BestDeal offers seamless integration with a chatbot, enabling users to interact naturally and obtain real-time assistance for their shopping needs.

## Features
1. Product Search: Users can search for products by keywords.
2. Price Comparison: The application displays prices from various online retailers for the searched product.
3. User-Friendly Interface: Intuitive design for easy navigation and usability.
4. Customization: Users can customize their search preferences and filter results.
5. Saved Searches: Users can save their searches for future reference.
6. Chatbot Integration: Real-time chatbot assistance for product inquiries and recommendations.

## Technology Stack
* Django
* Selenium
* Websockets (`channels` package)
* GPT4ALL

## Running the project
### Dependencies
```
pip install django selenium daphne channels
```
### Setting up the environment
Set the environment variable `BROWSER` to the path of the Brave browser.
#### For Windows
```
set BROWSER="path/to/brave"
```

#### For macOS (Fish shell)
```
set -Ux BROWSER '/Applications/Brave Browser.app
/Contents/MacOS/Brave Browser'
```
