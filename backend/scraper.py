from splinter import Browser
from bs4 import BeautifulSoup as soup
import time
import os
from dotenv import load_dotenv
from db import save_listing

# Load environment variables
load_dotenv()

EMAIL = os.getenv("FACEBOOK_EMAIL")
PASSWORD = os.getenv("FACEBOOK_PASSWORD")


def login_facebook(browser, email, password):
    browser.visit('https://www.facebook.com/login')
    browser.fill('email', email)
    browser.fill('pass', password)
    browser.find_by_name('login').click()
    
    # Wait for login
    time.sleep(5)
    if browser.is_element_present_by_css('[aria-label="Facebook"]', wait_time=10):
        print("Login successful!")
    else:
        print("Login failed. Check credentials.")
        browser.quit()
        exit()


def scrape_cars(make, model):
    with Browser('chrome') as browser:
        # Login
        login_facebook(browser, EMAIL, PASSWORD)
        
        # Navigate to Marketplace
        browser.visit('https://www.facebook.com/marketplace/calgary')
        time.sleep(5)
        
        # Search for cars
        if browser.is_element_present_by_css('[aria-label="Search Marketplace"]', wait_time=10):
            search_box = browser.find_by_css('[aria-label="Search Marketplace"]')
            search_box.fill(f'{make} {model}')
            search_box.first.type('\ue007')  # Press Enter
            time.sleep(5)
        
        # Scroll to load more results
        scroll_count = 4
        scroll_delay = 3
        for _ in range(scroll_count):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_delay)
        
        # Parse HTML
        html = browser.html
        market_soup = soup(html, 'html.parser')
        
        # Extract listings
        listings = []
        items = market_soup.find_all('div', {'role': 'article'})
        for item in items:
            try:
                title = item.find('span').text
                price = item.find('div', {'dir': 'auto'}).text
                link = item.find('a')['href']
                
                # Extract additional details
                details = item.find_all('span')
                location = details[1].text if len(details) > 1 else 'N/A'
                mileage = details[2].text if len(details) > 2 else 'N/A'
                year = details[3].text if len(details) > 3 else 'N/A'
                
                # Save to database
                save_listing(title, price, location, mileage, year, 'https://www.facebook.com' + link)
                
                listings.append({
                    'title': title,
                    'price': price,
                    'location': location,
                    'mileage': mileage,
                    'year': year,
                    'link': 'https://www.facebook.com' + link
                })
            except Exception as e:
                print(f"Error parsing item: {e}")
        
        return listings


if __name__ == '__main__':
    results = scrape_cars('Honda', 'Civic')
    if results:
        for res in results:
            print(res)
    else:
        print("No listings found.")

# Let me know if you’d like me to adjust anything else! 🚀
