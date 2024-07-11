# fastapi_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoengine import connect, Document, StringField, DateTimeField, URLField
from datetime import datetime

DATABASE_URL = "mongodb://localhost:27017/news_aggregator"

connect(host=DATABASE_URL)

app = FastAPI()

class Article(Document):
    title = StringField(required=True)
    source = StringField(required=True)
    author = StringField()
    published_at = DateTimeField()
    url_to_image = URLField()
    description = StringField()
    content = StringField()
    url = URLField(required=True)

class ArticleCreate(BaseModel):
    title: str
    source: str
    author: str
    published_at: datetime
    url_to_image: str
    description: str
    content: str
    url: str

@app.post("/articles/")
def create_article(article: ArticleCreate):
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
    article_doc.save()
    return article_doc.to_json()

@app.get("/articles/")
def read_articles(skip: int = 0, limit: int = 10):
    articles = Article.objects.skip(skip).limit(limit)
    return [article.to_json() for article in articles]


@app.delete("/articles/{article_id}")
def delete_article(article_id: str):
    article = Article.objects(id=article_id).first()
    if article:
        article.delete()
        return {"message": "Article deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Article not found")