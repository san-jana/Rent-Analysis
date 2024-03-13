from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import magicbricks

rental_prices = pd.DataFrame(columns = ['bhk','sqft_rent', 'rent', 'locality', 'city'])

def check_json(response):
    if "propertySearch.html" in response.url:
        for data in response.json()['resultList']:
            rental_prices.loc[len(rental_prices)] = [data['bedroomD'].split()[-1], data['sqFtPrice'], data['price'],
                                                     data['lmtDName'].split(',')[-1].strip(), data['ctName'].strip()]
            
       
cities = ['Noida', 'Mumbai', 'Pune', 'New Delhi', 'Kolkata', 'Ahmedabad', 'Jaipur']

for city in cities:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless = False)
    page = browser.new_page()
    page.goto(magicbricks.get_city_url(city))
    
    count = 0

    for i in range(100):
        if count == 3:
            break
        
        elif rental_prices.shape[0] > 3000:
            break
        
        locator = page.locator('xpath =//*[@id="pageLoader"]')
        if page.evaluate("window.pageYOffset") == page.evaluate("document.body.scrollHeight") and expect(locator).not_to_be_visible(timeout = 15000):
            count+=1
            print("count = ", count)
        
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        print("scrolled")
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_timeout(2000)      
        page.on('response', lambda response : check_json(response))
        print("loaded", i)
        print(rental_prices)       
        
    browser.close()
    playwright.stop()

rental_prices['bhk'] = rental_prices['bhk'].astype('int')
rental_prices['rent'] = rental_prices['rent'].astype('int')  

rental_prices.to_csv("C:\\Users\\Somu\\Desktop\\CDAC\\resources\\noida_data.csv", index = False)
