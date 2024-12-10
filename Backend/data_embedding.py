import re
import openai
from pymongo import MongoClient

# Set your OpenAI API key
openai.api_key = "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"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/newsarticle')
db = client["news_database"]  # Database name
articles_collection = db["news_articles"]  # Collection name

# Function to clean the article text (removes HTML tags and non-alphanumeric characters)
def clean_text(text):
    # Removing HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Removing non-alphanumeric characters (except spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()

# Function to generate embeddings using OpenAI's API
def generate_embedding(text):
    try:
        response = openai.embeddings.create(
            model="text-embedding-ada-002",  # Choose an appropriate embedding model
            input=text
        )
        # print(response.data[0].embedding)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Retrieve articles from MongoDB
articles_cursor = articles_collection.find()

# Process each article
for article in articles_cursor:
    # Step 1: Preprocess article content
    article_text = clean_text(article["description"])  # Using "description" field for the content
    
    # Step 2: Generate embedding for the article content
    article_embedding = generate_embedding(article_text)
    
    if article_embedding:  # Only update if embedding was successfully generated
        # Step 3: Store the generated embedding back in MongoDB
        article["embedding2"] = article_embedding
        
        # Update or insert the article with the embedding in the collection
        articles_collection.update_one(
            {"_id": article["_id"]},
            {"$set": {"embedding2": article_embedding}},
            upsert=True
        )
        print(f"Successfully added embedding for article: {article['title']}")
    else:
        print(f"Failed to generate embedding for article: {article['title']}")
