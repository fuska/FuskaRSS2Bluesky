from atproto import Client, client_utils
import feedparser
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import os
import time
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv
import sqlite3

# Load environment variables from .env file
load_dotenv()

# Set up environment variables
BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
RSS_FEED_URL = os.getenv("RSS_FEED_URL")

# Initialize the Bluesky client
client = Client()
client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)

# Set the minimum date for posting
MIN_POST_DATE = datetime(2024, 11, 13)


# Initialize the SQLite database
def initialize_database():
    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            published_date TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Check if the title is already in the database
def is_duplicate(title):
    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM posts WHERE title = ?", (title, ))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


# Insert a new post record into the database
def save_post(title, published_date):
    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, published_date) VALUES (?, ?)",
                   (title, published_date))
    conn.commit()
    conn.close()


def fetch_latest_rss_entry():
    """Fetches the latest entry from the RSS feed."""
    feed = feedparser.parse(RSS_FEED_URL)
    if feed.entries:
        return feed.entries[0]
    return None


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


def download_and_compress_image(image_url, max_size_kb=1000):
    """Downloads and compresses the image to be under the max_size_kb limit."""
    response = requests.get(image_url)
    if response.status_code != 200:
        print("Failed to download image:", response.status_code)
        return None

    image = Image.open(BytesIO(response.content))
    max_dimension = 1024
    if max(image.size) > max_dimension:
        image.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

    if image.format != "JPEG":
        image = image.convert("RGB")

    quality = 65
    output = BytesIO()
    image.save(output, format="JPEG", quality=quality, optimize=True)
    size_kb = output.tell() / 1024
    if size_kb > max_size_kb:
        print(
            f"Image too large even at lower quality. Final size: {size_kb:.2f} KB"
        )
        return None

    output.seek(0)
    return output.getvalue()


def create_post_with_image(entry):
    """Creates a post with an embedded image using the article's header image."""
    title = entry.title
    link = entry.link.rstrip('.html')

    # Parse the entry's published date and compare it to MIN_POST_DATE
    published_date = datetime(
        *entry.published_parsed[:6])  # Convert to datetime
    if published_date < MIN_POST_DATE:
        print("Entry published before minimum date. Skipping.")
        return

    # Check if the title has already been posted
    if is_duplicate(title):
        print("Post already exists in the database. Skipping.")
        return

    # Use TextBuilder to create rich text with a clickable link
    post_text = client_utils.TextBuilder().text(
        f"{title}\n\nRead more: ").link(link, link)

    # Fetch the article's header image
    image_url = fetch_image_url(link)
    if image_url:
        compressed_image_data = download_and_compress_image(image_url)
        if compressed_image_data:
            try:
                client.send_images(text=post_text,
                                   images=[compressed_image_data],
                                   image_alts=[title])
                print("Posted successfully with image!")
                save_post(title,
                          published_date.isoformat())  # Save to database
            except Exception as e:
                print("Failed to post with image:", str(e))
        else:
            print("No image data available after compression.")
    else:
        try:
            client.send_post(text=post_text)
            print("Posted successfully without image!")
            save_post(title, published_date.isoformat())  # Save to database
        except Exception as e:
            print("Failed to post text-only:", str(e))


def main():
    # Initialize the database
    initialize_database()

    while True:
        latest_entry = fetch_latest_rss_entry()
        if latest_entry:
            create_post_with_image(latest_entry)
        time.sleep(600)  # Check every 10 minutes


if __name__ == "__main__":
    main()
