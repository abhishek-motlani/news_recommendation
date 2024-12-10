from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter

# router2 = FastAPI()
router2=APIRouter()

# MongoDB setup
client = AsyncIOMotorClient('mongodb://localhost:27017/newsarticle')  # Use AsyncIOMotorClient
db = client["news_database"]

# Pydantic Models
class Article(BaseModel):
    _id: str
    url: str
    author: str
    category: str
    country: str
    description: str
    image: str
    language: str
    published_at: str
    source: str
    title: str

class UserInteraction(BaseModel):
    _id: str
    username: str
    article_id: str
    action: str
    action_type: str
    timestamp: str

class RecentArticle(BaseModel):
    article_id: str
    title: str
    published_at: str
    interactions: int

class CategoryInteraction(BaseModel):
    category: str
    interactions: int

class ActionBreakdown(BaseModel):
    action: str
    count: int

@router2.get("/articles/", response_model=List[Article])
async def get_articles():
    articles = await db.news_articles.find().to_list(100)
    return articles

@router2.get("/user-interactions/", response_model=List[UserInteraction])
async def get_user_interactions():
    interactions = await db.user_interactions.find().to_list(100)
    return interactions

@router2.get("/popular-articles/")
async def get_popular_articles():
    pipeline = [
        # Convert article_id from string to ObjectId for comparison
        {
            "$addFields": {
                "article_id": {"$toObjectId": "$article_id"}  # Convert article_id to ObjectId
            }
        },
        # Join user_interactions with articles collection based on article_id
        {
            "$lookup": {
                "from": "news_articles",  # Name of the articles collection
                "localField": "article_id",  # field from user_interactions
                "foreignField": "_id",  # field from news_articles
                "as": "article_details"  # Resulting array will be in 'article_details'
            }
        },
        # Unwind the article_details array so that each document has a single article's details
        {"$unwind": "$article_details"},
        # Group by article_id and sum likes
        {
            "$group": {
                "_id": "$article_id",
                "likes": {"$sum": {"$cond": [{"$eq": ["$action", "like"]}, 1, 0]}}
            }
        },
        # Lookup again to get the title of the article
        {
            "$lookup": {
                "from": "news_articles",  # Name of the articles collection
                "localField": "_id",  # article_id (from the group stage)
                "foreignField": "_id",  # field from news_articles
                "as": "article_details"
            }
        },
        # Unwind again to access the title
        {"$unwind": "$article_details"},
        # Project the desired fields (likes and title)
        {
            "$project": {
                "_id": 0,
                "title": "$article_details.title",
                "likes": 1
            }
        },
        # Sort by the likes count
        {"$sort": {"likes": -1}},
        {"$limit": 10}
    ]
    
    popular_articles = await db.user_interactions.aggregate(pipeline).to_list(10)
    return popular_articles

@router2.get("/user-stats/")
async def get_user_stats():
    pipeline = [
        {"$group": {"_id": "$username", "total_actions": {"$count": {}}}},
        {"$sort": {"total_actions": -1}}
    ]
    user_stats = await db.user_interactions.aggregate(pipeline).to_list(10)  # Works with async client
    return user_stats

@router2.get("/recent-articles/", response_model=List[RecentArticle])
async def get_recent_articles():
    pipeline = [
        {
            "$addFields": {
                "article_id": { "$toObjectId": "$article_id" }  # Convert the article_id from string to ObjectId
            }
        },
        {
            "$lookup": {
                "from": "news_articles",  # Join with the "news_articles" collection
                "localField": "article_id",  # Field in the "user_interactions" collection to join on (article_id)
                "foreignField": "_id",  # Field in the "news_articles" collection to match with (the unique article ID)
                "as": "article_details"  # The result will be stored as an array under the "article_details" field
            }
        },
        {
            "$unwind": "$article_details"  # Unwind the "article_details" array to access the article details
        },
        {
            "$group": {
                "_id": "$article_id",  # Group by the article_id
                "published_at": { "$first": "$article_details.published_at" },  # Get the first published_at from the article_details
                "interactions": { "$sum": 1 },  # Count the interactions for each article
                "title": { "$first": "$article_details.title" }  # Include the title of the article
            }
        },
        {
            "$sort": { "published_at": -1 }  # Sort by the published_at field in descending order (most recent first)
        },
        {
            "$limit": 10  # Limit the result to the top 10 articles
        }
    ]

    # Perform the aggregation query
    recent_articles = await db.user_interactions.aggregate(pipeline).to_list(10)

    # Convert MongoDB _id to string
    for article in recent_articles:
        article["article_id"] = str(article["_id"])
        del article["_id"]  # Remove _id field as it's not needed in the response

    return recent_articles

@router2.get("/category-interactions/", response_model=List[CategoryInteraction])
async def get_category_interactions():
    pipeline = [
        {
            "$addFields": {
                "article_id": { "$toObjectId": "$article_id" }  # Convert the article_id from string to ObjectId
            }
        },
        {
            "$lookup": {
                "from": "news_articles",  # Lookup to get the category from the articles collection
                "localField": "article_id",  # Field in user_interactions to join on
                "foreignField": "_id",  # Field in articles to join on
                "as": "article_details"
            }
        },
        {
            "$unwind": "$article_details"  # Unwind the article_details to get category
        },
        {
            "$group": {
                "_id": "$article_details.category",  # Group by article category
                "interactions": {"$sum": 1}  # Count interactions for each category
            }
        },
        {
            "$sort": {"interactions": -1}  # Sort by interactions in descending order
        }
    ]

    # Run the aggregation query
    category_interactions = await db.user_interactions.aggregate(pipeline).to_list(10)

    # Process the results and convert _id (category) to a string and return the response
    for category in category_interactions:
        category["category"] = category["_id"]
        del category["_id"]  # Remove _id since it's replaced with category field

    return category_interactions

@router2.get("/action-breakdown/", response_model=List[ActionBreakdown])
async def get_action_breakdown():
    pipeline = [
        {
            "$group": {
                "_id": "$action",  # Group by action (like, share, click, etc.)
                "count": {"$sum": 1}  # Count the occurrences of each action
            }
        },
        {
            "$sort": {"count": -1}  # Sort by action count in descending order
        }
    ]
    
    # Run the aggregation query
    action_breakdown = await db.user_interactions.aggregate(pipeline).to_list(10)

    # Process the result to match the response model structure
    for item in action_breakdown:
        item["action"] = item["_id"]  # Rename _id to action
        del item["_id"]  # Remove _id since it's not needed in the final response

    return action_breakdown
