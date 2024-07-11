import streamlit as st
import requests
import json
from datetime import date, datetime
from newsapi import NewsApiClient

API_URL = "http://localhost:8000"

def save_articles(article):
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
    response = requests.post(f"{API_URL}/articles/", json=article_data)
    if response.status_code == 200:
        st.toast("Article saved successfully!", icon="✅")
    else:
        st.toast("Failed to save article.", icon="❌")

def delete_article(article_id):
    response = requests.delete(f"{API_URL}/articles/{article_id}")
    if response.status_code == 200:
        st.success("Article removed successfully!")
    else:
        st.error("Failed to remove article.")

def get_saved_articles():
    response = requests.get(f"{API_URL}/articles/")
    if response.status_code == 200:
        return [json.loads(article) for article in response.json()]
    else:
        st.error("Failed to fetch saved articles.")
        return []

def display_articles(data, save_function=None):
    for article in data["articles"]:
        if article["title"] != "[Removed]":
            st.subheader(article["title"])

            col1, col2 = st.columns(2)
            with col1:
                st.write(f'**🔗 Source:** {article["source"]["name"]}')
                st.write(f'**📝 Author:** {article["author"]}')
            with col2:
                st.write(f'**🗓️ Published At:** {article["publishedAt"]}')
            
            if article["urlToImage"]:
                st.image(article["urlToImage"])
            st.write(article["description"])
            st.write(article["content"])
            st.link_button("🔗 Full Article", article['url'])

            if save_function:
                st.button("Save", on_click=save_function, args=(article,), type="primary", key=article['url'])
            st.markdown("---")

st.set_page_config(
    page_title="News Aggregator",
    page_icon="🔖",
    layout="centered",
    initial_sidebar_state="expanded",
)

COUNTRY_CODES = (
    'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb',
    'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl',
    'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua',
    'us', 've', 'za')

st.title('News Aggregator')

# Init
newsapi = NewsApiClient(api_key='168df166e7894f72828b7ac57ac04486')

st.sidebar.header("Search News")

with st.sidebar.expander("🔎 TOPIC", expanded=True):
    topic = st.text_input("Search", "Technology")
    topic = topic.strip()
    if not topic:
        st.warning("Please enter a valid topic!")

with st.sidebar.expander("🔝 TOP STORIES", expanded=True):
    category = st.selectbox('Category', ('Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'), index=4)
    country = st.selectbox('Country', COUNTRY_CODES, index=23)

with st.sidebar.expander("⚙️ Filters"):
    date_range = st.date_input("Period", value=(date(2024, 7, 1), date(2024, 7, 9)))
    sort = st.selectbox("Sort By", ("relevancy", "popularity", "publishedAt"))
    feed = st.slider('Story Feed', min_value=0, max_value=100, value=10, step=5)

tab_topic, tab_headlines, tab_saved = st.tabs(['🔎 Topic', '🔝 Top Stories', '🎫 Saved'])

if st.sidebar.button("Search"):
    with tab_topic:
        all_articles = newsapi.get_everything(q=topic, from_param=date_range[0], to=date_range[1], language='en', sort_by=sort, page_size=feed)
        display_articles(all_articles, save_function=save_articles)

    with tab_headlines:
        top_headlines = newsapi.get_top_headlines(category=category.lower(), language='en', country=country, page_size=feed)
        display_articles(top_headlines, save_function=save_articles)

with tab_saved:
    saved_articles = get_saved_articles()
    if not saved_articles:
        st.warning("No Saved Articles")
    for article in saved_articles:
        st.subheader(article["title"])

        col1, col2 = st.columns(2)
        with col1:
            st.write(f'**🔗 Source:** {article["source"]}')
            st.write(f'**📝 Author:** {article["author"]}')
        with col2:
            published_at = datetime.fromtimestamp(article["published_at"]["$date"] / 1000.0)  # Convert timestamp to datetime
            st.write(f'**🗓️ Published At:** {published_at}')

        if article["url_to_image"]:
            st.image(article["url_to_image"])
        st.write(article["description"])
        st.write(article["content"])
        st.link_button("🔗 Full Article", article['url'])
        st.button("Remove", on_click=delete_article, args=(article["_id"]["$oid"],), type="primary", key = article["_id"])
        st.markdown("---")