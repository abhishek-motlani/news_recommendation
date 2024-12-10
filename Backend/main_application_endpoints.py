from fastapi import HTTPException
from pydantic import BaseModel
from recommendation import get_query_embedding, get_all_article_embeddings_and_urls, recommend_similar_articles,get_personalized_recommendations
from pymongo import MongoClient
from fastapi import Request
from fastapi import APIRouter
from datetime import datetime

router1=APIRouter()

## Connecting to MongoDb to log 
# MongoDB Client Initialization
client = MongoClient('mongodb://localhost:27017/newsarticle')
db = client["news_database"]  # Use your database name
user_interactions_collection = db.user_interactions

# Input model for query
class Query(BaseModel):
    text: str

# API endpoint to recommend articles
@router1.post("/recommend")
async def recommend_articles(query: Query):
    try:
        # Compute embedding for the query
        query_embedding = get_query_embedding(query.text)
        
        # Retrieve all embeddings and URLs from MongoDB
        article_embeddings, article_urls, article_titles, article_description,article_id = get_all_article_embeddings_and_urls()
        
        # Get the top 5 similar articles
        recommendations = recommend_similar_articles(
            query_embedding,
            article_embeddings,
            article_urls,
            article_titles,
            article_description,
            article_id
        )
       
        structured_recommendations = [
            {
                "label": f"Recommendation {i + 1}",
                "title": rec[0],
                "description": rec[1],
                "url": rec[2],
                "id":str(rec[3]),
                "similarity_score": f"{rec[4]:.4f}"
            }
            for i, rec in enumerate(recommendations)
        ]

        return {"query": query.text, "recommendations": structured_recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Input model for logging interaction
class UserInteraction(BaseModel):
    username: str
    article_id: str
    action: str  # 'like' or 'dislike'
    action_type:str

## Logging for recommending personalised news
@router1.post("/log_interaction")
async def log_interaction(interaction: UserInteraction, request: Request):
    # raw_body = await request.json()
    # print("Raw Request Body:", raw_body)  # Log the raw request for debugging
    # print("Incoming Data:", interaction)

    try:    
        # Log the user interaction in MongoDB
        interaction_data = {
            "username": interaction.username,
            "article_id": interaction.article_id,
            "action": interaction.action,  # 'like' or 'dislike'
            "action_type":interaction.action_type,
            "timestamp": datetime.now()
        }
        user_interactions_collection.insert_one(interaction_data)
        return {"message": "Interaction logged successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
##personalised recommendation
@router1.post("/personal_recommend")
async def recommend_personalized_articles(user_name: Query):
    try:
        # print(user_name.text)
        # Get personalized recommendations based on the username
        recommendations = get_personalized_recommendations(user_name.text)

        if not recommendations:
            raise HTTPException(status_code=404, detail="No personalized recommendations available.")
        
        structured_recommendations = [
            {
                "label": f"Recommendation {i + 1}",
                "title": rec[0],
                "description": rec[1],
                "url": rec[2],
                "id": str(rec[3]),
                "similarity_score": f"{rec[4]:.4f}"
            }
            for i, rec in enumerate(recommendations)
        ]
        # print(structured_recommendations)
        return {"username": user_name.text, "recommendations": structured_recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))