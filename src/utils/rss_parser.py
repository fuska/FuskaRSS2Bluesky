import feedparser
from datetime import datetime

def fetch_new_rss_entries(db_handler):
    """Fetch new RSS entries that haven’t been posted yet."""
    feed = feedparser.parse("https://chicagoyimby.com/feed")
    new_entries = []

    for entry in feed.entries:
        title = entry.title
        published = datetime(*entry.published_parsed[:6])  # Convert to datetime

        # Only add entries that haven't been posted and are recent
        if not db_handler.is_posted(title) and published >= datetime(2024, 11, 13):
            # Add image URL if available
            entry.image_url = entry.get("image_url", None)
            new_entries.append(entry)

    return new_entries
