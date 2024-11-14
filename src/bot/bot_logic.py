import time
from atproto import Client
from bot.db_handler import DatabaseHandler
from bot.post_handler import PostHandler
from utils import fetch_new_rss_entries
from config import BLUESKY_USERNAME, BLUESKY_PASSWORD

class BotLogic:
    def __init__(self, interval=600, max_retries=5, initial_delay=10):
        self.db_handler = DatabaseHandler()
        self.client = Client()
        self.interval = interval  # Interval in seconds
        self.max_retries = max_retries
        self.initial_delay = initial_delay

        # Try to log in with exponential backoff
        self._login_with_retries()

        # Pass the logged-in client to PostHandler
        self.post_handler = PostHandler(self.client)

    def _login_with_retries(self):
        retries = 0
        delay = self.initial_delay
        while retries < self.max_retries:
            try:
                self.client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
                print("Logged in successfully!")
                return  # Exit if login is successful
            except Exception as e:
                print(f"Login attempt {retries + 1} failed: {e}")
                if "RateLimitExceeded" in str(e):
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                    retries += 1
                else:
                    raise e  # Raise other exceptions
        raise Exception("Max retries exceeded. Could not log in to Bluesky.")

    def run(self):
        """Run the bot continuously at the specified interval."""
        while True:
            new_entries = fetch_new_rss_entries(self.db_handler)
            for entry in new_entries:
                self.post_handler.post_entry(entry)
                self.db_handler.save_post(entry.title, entry.published)
            time.sleep(self.interval)  # Wait before the next run
