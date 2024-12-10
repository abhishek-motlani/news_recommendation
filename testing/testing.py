# from pymongo import MongoClient
# from bson import ObjectId

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/newsarticle")
# db = client["news_database"]
# # Get the collections
# user_interactions = db.user_interactions
# news_articles = db.news_articles

# # Aggregation pipeline
# pipeline = [
#     {
#         "$addFields": {
#             "article_id": { "$toObjectId": "$article_id" }  # Convert the article_id from string to ObjectId
#         }
#     },
#     {
#         "$lookup": {
#             "from": "news_articles",  # Join with the "news_articles" collection
#             "localField": "article_id",  # Field in the "user_interactions" collection to join on (article_id)
#             "foreignField": "_id",  # Field in the "news_articles" collection to match with (the unique article ID)
#             "as": "article_details"  # The result will be stored as an array under the "article_details" field
#         }
#     },
#     {
#         "$unwind": "$article_details"  # Unwind the "article_details" array to access the article details
#     },
#     {
#         "$group": {
#             "_id": "$article_id",  # Group by the article_id
#             "published_at": { "$first": "$article_details.published_at" },  # Get the first published_at from the article_details
#             "interactions": { "$sum": 1 }  # Count the interactions for each article
#         }
#     },
#     {
#         "$sort": { "published_at": -1 }  # Sort by the published_at field in descending order (most recent first)
#     },
#     {
#         "$limit": 10  # Limit the result to the top 10 articles
#     }
# ]

# # Run the aggregation
# result = list(user_interactions.aggregate(pipeline))

# # Print the results
# for item in result:
#     print(item)