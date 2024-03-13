from bs4 import BeautifulSoup
import requests


def get_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html')
    return soup

def get_next_page(soup):
    page = soup.find('ul', class_ = 'mb-pagination__list')
    if not page.find('li', class_ = 'mb-pagination--next disabled'):
        url = 'https://www.magicbricks.com/'+ str((page.find('li', class_ = 'mb-pagination--next')).find('a')['href'])
        return url
    
    else:
        return