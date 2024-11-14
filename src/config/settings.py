import os
from dotenv import load_dotenv

load_dotenv()

BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
RSS_FEED_URL = os.getenv("RSS_FEED_URL")
