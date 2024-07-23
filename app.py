# Import necessary libraries and modules
import streamlit as st
import requests
import json
from datetime import date, datetime
from newsapi import NewsApiClient

# URL for the backend FastAPI application
API_URL = "http://localhost:8000"

# Define a function to save an article by sending a POST request to the backend
def save_articles(article):
    # Create a dictionary with the article data
    article_data = {
        "title": article["title"],
        "source": article["source"]["name"],
        "author": article["author"],
        "published_at": article["publishedAt"],
        "url_to_image": article["urlToImage"],
        "description": article["description"],
        "content": article["content"],
        "url": article["url"]
    }
    # Send a POST request to save the article
    response = requests.post(f"{API_URL}/articles/", json=article_data)
    # Display a toast notification based on the response status
    if response.status_code == 200:
        st.toast("Article saved successfully!", icon="✅")
    else:
        st.toast("Failed to save article.", icon="❌")

# Define a function to delete an article by sending a DELETE request to the backend
def delete_article(article_id):
    # Send a DELETE request to remove the article
    response = requests.delete(f"{API_URL}/articles/{article_id}")
    # Display a success or error message based on the response status
    if response.status_code == 200:
        st.success("Article removed successfully!")
    else:
        st.error("Failed to remove article.")

# Define a function to retrieve saved articles by sending a GET request to the backend
def get_saved_articles():
    # Send a GET request to fetch the saved articles
    response = requests.get(f"{API_URL}/articles/")
    # If the response is successful, return the list of articles
    if response.status_code == 200:
        return [json.loads(article) for article in response.json()]
    # If the response fails, display an error message and return an empty list
    else:
        st.error("Failed to fetch saved articles.")
        return []

# Define a function to display articles
def display_articles(data, save_function=None):
    # Iterate over each article in the provided data
    for article in data["articles"]:
        # Skip articles with the title "[Removed]"
        if article["title"] != "[Removed]":
            st.subheader(article["title"])

            # Create two columns for displaying article metadata
            col1, col2 = st.columns(2)
            with col1:
                st.write(f'**🔗 Source:** {article["source"]["name"]}')
                st.write(f'**📝 Author:** {article["author"]}')
            with col2:
                st.write(f'**🗓️ Published At:** {article["publishedAt"]}')
            
            # Display the article image if available
            if article["urlToImage"]:
                st.image(article["urlToImage"])
            # Display the article description and content
            st.write(article["description"])
            st.write(article["content"])
            st.link_button("🔗 Full Article", article['url'])

            # If a save function is provided, add a "Save" button for each article
            if save_function:
                st.button("Save", on_click=save_function, args=(article,), type="primary", key=article['url'])
            st.markdown("---")

# Set the page configuration for the Streamlit application
st.set_page_config(
    page_title="News Aggregator",  # Title of the page
    page_icon="🔖",  # Icon for the page
    layout="centered",  # Layout style
    initial_sidebar_state="expanded",  # Initial state of the sidebar
)

# Define the list of country codes for news sources
COUNTRY_CODES = (
    'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb',
    'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl',
    'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua',
    'us', 've', 'za')

# Display the main title of the application
st.title('News Aggregator')

# Initialize the NewsAPI client with the API key
newsapi = NewsApiClient(api_key='168df166e7894f72828b7ac57ac04486')

# Sidebar header for search options
st.sidebar.header("Search News")

# Sidebar expander for topic search
with st.sidebar.expander("🔎 TOPIC", expanded=True):
    # Text input for the topic search
    topic = st.text_input("Search", "Technology")
    topic = topic.strip()
    if not topic:
        st.warning("Please enter a valid topic!")

# Sidebar expander for top stories
with st.sidebar.expander("🔝 TOP STORIES", expanded=True):
    # Dropdown for selecting news category
    category = st.selectbox('Category', ('Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'), index=4)
    # Dropdown for selecting country
    country = st.selectbox('Country', COUNTRY_CODES, index=23)

# Sidebar expander for additional filters
with st.sidebar.expander("⚙️ Filters"):
    # Date input for selecting the period
    date_range = st.date_input("Period", value=(date(2024, 7, 19), date(2024, 7, 22)))
    # Dropdown for selecting sort order
    sort = st.selectbox("Sort By", ("relevancy", "popularity", "publishedAt"))
    # Slider for selecting the number of articles to fetch
    feed = st.slider('Story Feed', min_value=0, max_value=100, value=10, step=5)

# Define tabs for different sections of the application
tab_topic, tab_headlines, tab_saved = st.tabs(['🔎 Topic', '🔝 Top Stories', '🎫 Saved'])

# Button to trigger the search
if st.sidebar.button("Search"):
    with tab_topic:
        # Fetch articles based on the topic search
        all_articles = newsapi.get_everything(q=topic, from_param=date_range[0], to=date_range[1], language='en', sort_by=sort, page_size=feed)
        # Display the fetched articles using the display function
        display_articles(all_articles, save_function=save_articles)

        with tab_headlines:
            # Fetch top headlines based on the selected category and country
            top_headlines = newsapi.get_top_headlines(category=category.lower(), language='en', country=country, page_size=feed)
            # Display the fetched top headlines using the display function
            display_articles(top_headlines, save_function=save_articles)



# Display saved articles in the "Saved" tab
with tab_saved:
    # Retrieve the saved articles from the backend
    saved_articles = get_saved_articles()
    # If there are no saved articles, display a warning message
    if not saved_articles:
        st.warning("No Saved Articles")
    # Iterate over each saved article and display its details
    for article in saved_articles:
        st.subheader(article["title"])

        # Create two columns for displaying article metadata
        col1, col2 = st.columns(2)
        with col1:
            st.write(f'**🔗 Source:** {article["source"]}')
            st.write(f'**📝 Author:** {article["author"]}')
        with col2:
            # Convert the published_at timestamp to a readable datetime format
            published_at = datetime.fromtimestamp(article["published_at"]["$date"] / 1000.0)
            st.write(f'**🗓️ Published At:** {published_at}')

        # Display the article image if available
        if article["url_to_image"]:
            st.image(article["url_to_image"])
        # Display the article description and content
        st.write(article["description"])
        st.write(article["content"])
        # Provide a link to the full article
        st.link_button("🔗 Full Article", article['url'])
        # Add a button to remove the article, calling the delete_article function
        st.button("Remove", on_click=delete_article, args=(article["_id"]["$oid"],), type="primary", key=article["_id"])
        st.markdown("---")