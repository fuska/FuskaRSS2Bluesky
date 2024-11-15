import feedparser
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from settings import MIN_POST_DATE  # Import the minimum post date

def fetch_new_rss_entries(db_handler):
    """Fetch new RSS entries that haven’t been posted yet."""
    feed = feedparser.parse("https://chicagoyimby.com/feed")
    new_entries = []

    for entry in feed.entries:
        title = entry.title
        published = datetime(*entry.published_parsed[:6])  # Convert to datetime

        # Only add entries that haven't been posted and are recent
        if not db_handler.is_posted(title) and published >= MIN_POST_DATE:
            # Fetch the image URL from the article page
            image_url = fetch_image_url(entry.link)
            entry.image_url = image_url
            new_entries.append(entry)

    return new_entries

def fetch_image_url(article_url):
    """Extracts the header image URL from the article page."""
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tag = soup.find('meta', property='og:image') or soup.find('img')
    if image_tag and image_tag.get('content'):
        return image_tag['content']
    elif image_tag and image_tag.get('src'):
        return image_tag['src']
    return None
