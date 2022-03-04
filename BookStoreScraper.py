import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def getBookDocument(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    for section in soup.find('ol').find_all('li'):
        for a in section.find('h3'):
            bookName = a['title']

        ratingMapping = {
            'One': 1, 
            'Two': 2, 
            'Three': 3, 
            'Four': 4, 
            'Five': 5
        }
        starRating = section.find('p')['class'][1]
        rating = ratingMapping[starRating]

        prodPriceClass = section.find('div', {'class': 'product_price'})
        for p in prodPriceClass.find('p', {'class': 'price_color'}):
            bookPrice = p[1::]
        
        prodInStock = prodPriceClass.find('p', {'class': 'instock availability'}).contents[2].strip()

        bookJson = json.dumps(
            {
                'Title': bookName,
                'Rating': rating,
                'Price (GBP)': bookPrice,
                'In-Stock Status': prodInStock,
                'Scrape Date': datetime.now().isoformat()
            }
        )
    
    return bookJson





# for url in url_list: 
#     do the thing above ^^^

def getURLList(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    sidebar = soup.find('div', {'class': 'side_categories'}).find('ul').find('ul')

    for i in sidebar.find_all('li'):
        print(i.find('a')['href'])
        print(i.find('a').contents[0].strip())

    return sidebar.prettify()

print(getURLList('https://books.toscrape.com/index.html'))
