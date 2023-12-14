from selenium import webdriver

def extract_prices_with_selenium(driver):
    # Find the <meta> tag with itemprop="price"
    meta_tag = driver.find_element_by_xpath('//meta[@itemprop="price"]')

    # Get the value of the content attribute
    price = meta_tag.get_attribute('content')

    return price

def scrape_prices(url, user_agent):
    # Create a new instance of the Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Extract price data using Selenium
        price = extract_prices_with_selenium(driver)

        # Display the scraped price data
        print("Scraped Price:", price)
    finally:
        # Close the browser window
        driver.quit()

# Example usage:
url_to_scrape = 'https://example-store.com/products'
user_agent_windows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'

prices_windows = scrape_prices(url_to_scrape, user_agent_windows)
