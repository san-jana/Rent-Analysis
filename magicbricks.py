from bs4 import BeautifulSoup
import requests

def get_city_url(city_name):
    ''' Get the url specific to the rental data of the user entered city from the magic bricks webdata.
    If the city entered exists in the Magic Bricks rental database, a url is returned, else the user is notified that such a city does not exist in the database.
    
    Parameters - 
    city_name(string) : Name of a city in India.
    
    Separate any city name's prefixes or postfixes with a space.
    Eg.: Navi Mumbai, Delhi Ncr, New Delhi.
    
    Returns a Magic Bricks url to the rental webpage of that city.
    '''
    
    # Magic bricks base url for residential rooms on rent
    magic_bricks_url='https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName='
    
    # Generating url for the user input city (the city name is concatenated with the base url in the title case)  
    city = "-".join(list(map(str.title , city_name.split())))
    magic_bricks_city_url = magic_bricks_url + city
    
    # checking whether the webpage for the entered city exists 
    ''' if the webpage for any city exists, the webpage contains a div tag 
    with a 'mb-header__container mb-header__main__section pos-rel' class 
    (which is used to create a header container in the webpage) 
    in its html encoding and returns a list of all the html data within the div. 
    If the webpage does not exist, then an empty list is returned instead. 
    '''
    page = requests.get(magic_bricks_city_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    check = soup.find_all('div', class_ = 'mb-header__container mb-header__main__section pos-rel')

    # if the webpage does not exist, then notify the user about the wrong entry
    if not check:
        return print('This city does not exist! Check for spelling errors or try a different city.')
    
    # otherwise return the city specific url
    return magic_bricks_city_url
  