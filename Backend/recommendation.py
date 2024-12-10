from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from bson import ObjectId

import openai

# Set your OpenAI API key
openai.api_key = "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"

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/newsarticle')
db = client["news_database"]  # Database name
articles_collection = db["news_articles"]  # Collection name
user_actions_collection = db["user_interactions"]

# Function to get all article embeddings and URLs from MongoDB
def get_all_article_embeddings_and_urls():
    # Retrieve all articles' embeddings and URLs from MongoDB
    cursor = articles_collection.find({}, {"title":1, "description": 1,"embedding2": 1, "url": 1,"_id":1})
    article_embeddings = []
    article_urls = []
    article_titles=[]
    article_description=[]
    article_id=[]
    
    for article in cursor:
        article_embeddings.append(np.array(article['embedding2']))  # Assuming embedding is a list/array
        article_urls.append(article['url'])
        article_titles.append(article['title'])
        article_description.append(article['description'])
        article_id.append(article['_id'])
    
    # print(len(article_description))
    # print(len(article_id))
    # print("0th:" , article_id[0])
    return np.array(article_embeddings), article_urls, article_titles, article_description,article_id

def get_query_embedding(query_article):
    # Use OpenAI's API to get the embedding for the query article
    response = openai.embeddings.create(
        model="text-embedding-ada-002",  # You can use other models too
        input=query_article
    )
    # Return as a numpy array
    return np.array(response.data[0].embedding).reshape(1, -1)



# Function to recommend similar articles based on a query embedding
def recommend_similar_articles(query_embedding, article_embeddings, article_urls, article_titles, article_description, article_id,top_n=5):
    #print("article_id:", article_id[0])
    # Compute cosine similarities between the query and all stored article embeddings
    similarities = cosine_similarity(query_embedding, article_embeddings)
    
    # Flatten the similarity array and sort indices based on similarity score
    sorted_indices = np.argsort(similarities[0])[::-1]  # Sort in descending order
    
    # Get top N similar articles and their URLs
    recommended_articles = [(article_titles[i], article_description[i], article_urls[i], article_id[i], similarities[0][i]) for i in sorted_indices[:top_n]]
    # print(recommended_articles)
    
    return recommended_articles

##Personalised recommendation
# Function to generate personalized recommendations based on user actions
def get_personalized_recommendations(username, top_n=15):
    
    # Fetch user's recent interactions
    user_interactions = user_actions_collection.find({"username": username})
    
    liked_articles = [interaction["article_id"] for interaction in user_interactions if interaction["action"] == "like" or interaction["action"]=='read_more']
    # print(liked_articles)
    if not liked_articles:
        print("No personalized data available. Showing generic recommendations.")
        return None

    # Fetch embeddings for liked articles
    liked_embeddings = []
    for article_id in liked_articles:
        article_id_obj = ObjectId(article_id)
        article = articles_collection.find_one({"_id": article_id_obj}, {"embedding2": 1})
        if article:
            liked_embeddings.append(np.array(article["embedding2"]))
    print("getting called")
    if not liked_embeddings:
        print("Could not find embeddings for liked articles.")
        return None

    # Calculate average embedding for liked articles
    user_profile_embedding = np.mean(liked_embeddings, axis=0).reshape(1, -1)
    
    # Get all article embeddings
    article_embeddings, article_urls, article_titles, article_description, article_id = get_all_article_embeddings_and_urls()
    
    # Recommend similar articles
    recommended_articles = recommend_similar_articles(
        user_profile_embedding, article_embeddings, article_urls, article_titles, article_description, article_id, top_n
    )
    print(recommended_articles)
    return recommended_articles




#### Testing purpose
# # Example usage
# query_article = "Latest technology"  # This can be the query article's text
# query_embedding = get_query_embedding(query_article)

# # Retrieve all embeddings and URLs from MongoDB
# article_embeddings, article_urls, article_titles, article_description = get_all_article_embeddings_and_urls()

# # Get the top 5 similar articles
# recommended_articles = recommend_similar_articles(query_embedding, article_embeddings, article_urls, article_titles, article_description)

# # Print the recommended articles with their URLs and similarity scores
# for title, description, url, similarity in recommended_articles:
#     print(f"Title: {title}")
#     print(f"Description: {description}")
#     print(f"Recommended URL: {url}, Similarity Score: {similarity:.4f}")
