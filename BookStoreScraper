import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

resp = requests.get(url)

soup = BeautifulSoup(resp.content, "html.parser")

for section in soup.find('ol').find_all('li'):
    for a in section.find('h3'):
        bookName = a['title']
        print(bookName)

    ratingMapping = {
        'One': 1, 
        'Two': 2, 
        'Three': 3, 
        'Four': 4, 
        'Five': 5
    }
    starRating = section.find('p')['class'][1]
    rating = ratingMapping[starRating]
    print(rating)

    prodPriceClass = section.find('div', {'class': 'product_price'})
    for p in prodPriceClass.find('p', {'class': 'price_color'}):
        bookPrice = p[1::]
        print(bookPrice)
    
    prodInStock = prodPriceClass.find('p', {'class': 'instock availability'}).contents[2].strip()
    print(prodInStock)

    asJson = json.dumps(
        {
            'Title': bookName,
            'Rating': rating,
            'Price (GBP)': bookPrice,
            'In-Stock Status': prodInStock,
            'Scrape Date': datetime.now().isoformat()
        }
    )

    print(asJson)
    print('\n')