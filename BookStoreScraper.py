from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def getMongoCollection(uri, db, collection):
    client = MongoClient(uri)
    dbase = client[db]
    collObj = dbase[collection]
    print(collObj.find_one())

    return collObj


def getGenresAndURLs(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    sidebar = soup.find('div', {'class': 'side_categories'}).find('ul').find('ul')
    urlAndGenre = []

    for i in sidebar.find_all('li'):
        urlAndGenre.append((i.find('a').contents[0].strip(), 'https://books.toscrape.com/' + i.find('a')['href']))

    return urlAndGenre


def getBookDocuments(genre, url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    listOfJSON = []

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
                'Genre': genre,
                'Rating': rating,
                'Price (GBP)': bookPrice,
                'In-Stock Status': prodInStock,
                'Scrape Date': datetime.now().isoformat()
            }
        )

        listOfJSON.append(bookJson)
    
    return listOfJSON

def main():
    homePageURL = 'https://books.toscrape.com/'
    mongoURI = 'mongodb+srv://cameronjcyr:Kotaleo1216!@prodcluster.85gfh.mongodb.net/'
    db = 'BookStore'
    collection = 'Books'
    allBooks = []

    genresURLsTuples = getGenresAndURLs(homePageURL)
    booksColl = getMongoCollection(mongoURI, db, collection)

    for i in genresURLsTuples:
        allBooks.append((i[0], getBookDocuments(i[0], i[1])))
        

if __name__ == "__main__":
    main()