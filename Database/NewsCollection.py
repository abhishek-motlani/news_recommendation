import requests
import pandas as pd
from pymongo import MongoClient
import time
from pymongo.errors import DuplicateKeyError

# MediaStack API credentials
API_KEY = "c02a23329fada2bff4ab17aab4b37763"  # Replace with your API key
BASE_URL = "http://api.mediastack.com/v1/news"

## Creating a Database and collection 
MONGO_URL = 'mongodb://localhost:27017/newsarticle'

client = MongoClient(MONGO_URL)
db = client['news_database']
collection = db['news_articles']

# Create a unique index on the 'url' field to prevent duplicates
collection.create_index([('url', 1)], unique=True)

# Function to fetch news data
def fetch_news_data(keywords, languages="en", countries="us", total_articles=1000):
    """
    Fetch news articles from MediaStack API based on keywords, language, and country.
    :param keywords: List of keywords to search for.
    :param languages: Language of the articles (default: English).
    :param countries: Country code for the articles (default: US).
    :param limit: Number of articles to retrieve.
    :return: List of news articles.
    """
    articles = []
    fetched_articles = 0
    limit = 100
    while fetched_articles < total_articles:

        for keyword in keywords:
            params = {
                "access_key": API_KEY,
                "keywords": keyword,
                "languages": languages,
                "countries": countries,
                "limit": limit,
                "offset": fetched_articles
            }
            try:
                response = requests.get(BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if "data" in data:
                        articles.extend(data["data"])
                        fetched_articles += len(articles)
                        print(f"Fetched {fetched_articles} articles so far...")

                        insert_articles_to_mongo(articles)
                    else:
                        print(f"No data found for keyword: {keyword}")
                else:
                    print(f"Failed to fetch data for {keyword}. HTTP Status: {response.status_code}")
            except Exception as e:
                print(f"Error fetching data for {keyword}: {e}")
            
            ## pause to avoid hitting rate limits
            time.sleep(1)

        ## if fetched enough articles break the loop
        if fetched_articles >= total_articles:
            break

    return articles

# Inserting data to database (upsert to avoid duplicates)
def insert_articles_to_mongo(articles):
    if articles:
        for article in articles:
            try:
                # Use upsert: if an article with the same URL exists, update it; otherwise, insert the new article
                collection.update_one(
                    {'url': article['url']},  # Unique field (e.g., URL)
                    {'$set': article},  # Update the article
                    upsert=True  # Insert if not found, update if exists
                )
                print(f"Inserted or updated article with URL: {article['url']}")
            except DuplicateKeyError:
                print(f"Duplicate article with URL {article['url']} found, skipping.")
            except Exception as e:
                print(f"Error inserting/updating article: {e}")
    else:
        print("No articles to insert.")

# Main script
if __name__ == "__main__":
    # Define your search parameters
    keywords = ["technology", "science", "business", "entertainment", "health", "sport"]  # Replace with desired topics
    articles = fetch_news_data(keywords=keywords, total_articles=1000)
