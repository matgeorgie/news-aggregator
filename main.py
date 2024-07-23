# Import necessary libraries and modules
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoengine import connect, Document, StringField, DateTimeField, URLField
from datetime import datetime

# URL for the MongoDB database connection
DATABASE_URL = "mongodb://localhost:27017/news_aggregator"

# Connect to the MongoDB database using the provided URL
connect(host=DATABASE_URL)

# Initialize a FastAPI application
app = FastAPI()

# Define a MongoDB document schema for storing articles
class Article(Document):
    title = StringField(required=True)  
    source = StringField(required=True)  
    author = StringField()  
    published_at = DateTimeField() 
    url_to_image = URLField()
    description = StringField()
    content = StringField()
    url = URLField(required=True)

# Define a Pydantic model for validating article creation requests
class ArticleCreate(BaseModel):
    title: str  
    source: str 
    author: str
    published_at: datetime
    url_to_image: str
    description: str 
    content: str  
    url: str  #

# Define an endpoint to create and save a new article
@app.post("/articles/")
def create_article(article: ArticleCreate):
    # Create a new Article document using the data from the request
    article_doc = Article(
        title=article.title,
        source=article.source,
        author=article.author,
        published_at=article.published_at,
        url_to_image=article.url_to_image,
        description=article.description,
        content=article.content,
        url=article.url
    )
    # Save the Article document to the database
    article_doc.save()
    # Return the saved Article document as a JSON response
    return article_doc.to_json()

# Define an endpoint to retrieve saved articles with pagination
@app.get("/articles/")
def read_articles(skip: int = 0, limit: int = 10):
    # Retrieve a list of Article documents from the database with pagination
    articles = Article.objects.skip(skip).limit(limit)
    # Return the list of articles as a JSON response
    return [article.to_json() for article in articles]

# Define an endpoint to delete an article by its ID
@app.delete("/articles/{article_id}")
def delete_article(article_id: str):
    # Retrieve the Article document with the specified ID from the database
    article = Article.objects(id=article_id).first()
    # If the article exists, delete it and return a success message
    if article:
        article.delete()
        return {"message": "Article deleted successfully"}
    # If the article does not exist, raise a 404 HTTP exception
    else:
        raise HTTPException(status_code=404, detail="Article not found")
