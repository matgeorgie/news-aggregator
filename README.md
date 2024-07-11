# News Aggregator

A Streamlit-based news aggregator app that allows users to search for and display news articles based on various topics, categories, and countries. Users can save articles of interest and delete them as needed.

## Features

- Search for news articles by topic.
- View top headlines by category and country.
- Save articles to a local database.
- Delete saved articles.


## Configuration

1. Obtain an API key from [NewsAPI](https://newsapi.org/).
2. Set up a local server to handle article storage and retrieval. Make sure the server is running at `http://localhost:8000`.

## Usage

1. Run the FastAPI & Streamlit app:
    ```bash
    fastapi run main.py
    streamlit run app.py
    ```
2. Start a MongoDB Local Connection
3. Open your browser and go to `http://localhost:8501` to access the News Aggregator app.

## API Endpoints

- `POST /articles/` - Save a new article.
- `DELETE /articles/{article_id}` - Delete an article by ID.
- `GET /articles/` - Retrieve all saved articles.
