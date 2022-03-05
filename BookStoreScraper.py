from pyclbr import Class
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import os


def getMongoCollection(uri: str, db: str, collection: str) -> Class:
    """
    Returns a MongoDB collection object for a give Database and Collection.\n
    Keyword Arguments:\n    
    uri -- MongoDB URI Connection String \n
    db -- Name of the MongoDB Database (type) \n
    collection -- Name of the MongoDB Collection
    """

    client = MongoClient(uri)
    dbase = client[db]
    collObj = dbase[collection]

    return collObj


def getGenresAndURLs(url: str) -> list:
    """
    Returns a list of tuples (Genre, URL) based on the provided url.\n
    Keyword Arguments:\n
    url -- the home page of books.toscrape.com
    """
    
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    sidebar = soup.find('div', {'class': 'side_categories'}).find('ul').find('ul')
    urlAndGenre = []

    for i in sidebar.find_all('li'):
        urlAndGenre.append((i.find('a').contents[0].strip(), 'https://books.toscrape.com/' + i.find('a')['href']))

    return urlAndGenre


def getBookDocuments(genre: str, url: str) -> list:
    """
    Returns a list of dictionaries.\n
    Each dictionary contains the scraped data for one book in the bookstore.\n
    Keyword Arguments:\n
    genre -- genre of the books under the provided url\n
    url -- url related to a certain genre of books
    """
    
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

        bookJson = {
            'Title': bookName,
            'Genre': genre,
            'Rating': rating,
            'Price (GBP)': bookPrice,
            'In-Stock Status': prodInStock,
            'Scrape Date': datetime.now().isoformat()
        }

        listOfJSON.append(bookJson)
    
    return listOfJSON


def main():
    load_dotenv()
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_PORT = os.getenv("MONGO_PORT")

    homePageURL = 'https://books.toscrape.com/'
    mongoURI = 'mongodb+srv://{}:{}@prodcluster.{}.mongodb.net/'.format(MONGO_USERNAME, MONGO_PASSWORD, MONGO_PORT)
    db = 'BookStore'
    collection = 'Books'

    genresURLsTuples = getGenresAndURLs(homePageURL)
    booksColl = getMongoCollection(mongoURI, db, collection)

    for tup in genresURLsTuples:
        documents = getBookDocuments(tup[0], tup[1])
        
        for doc in documents:
            booksColl.replace_one(
                {'Title': doc['Title']},
                doc,
                upsert = True
            )


if __name__ == "__main__":
    main()