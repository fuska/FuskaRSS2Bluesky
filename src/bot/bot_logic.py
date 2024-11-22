import time
import yaml
import os
from datetime import datetime
from atproto import Client
from bot.post_handler import PostHandler
from bot.db_handler import DatabaseHandler
from utils.rss_parser import fetch_new_rss_entries
import logging
from typing import List
from dotenv import load_dotenv

class BotLogic:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.config = self._load_config()
        
        # Initialize client and settings
        self.client = Client()
        self.interval = self.config['bot']['check_interval']
        self.max_retries = self.config['bot']['max_retries']
        self.initial_delay = self.config['bot']['initial_delay']
        
        # Initialize database handler if database checking is enabled
        if self.config['bot']['duplicate_detection']['check_database']:
            self.db_handler = DatabaseHandler()
        else:
            self.db_handler = None
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, self.config['logging']['level']),
            format=self.config['logging']['format']
        )
        self.logger = logging.getLogger(__name__)

        # Try to log in with exponential backoff
        self._login_with_retries()

        # Pass the logged-in client to PostHandler
        self.post_handler = PostHandler(self.client)

    def _load_config(self):
        """Load configuration from YAML file."""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '../../config.yaml')
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.critical(f"Failed to load config file: {e}")
            raise

    def _login_with_retries(self):
        """Attempt to log in with exponential backoff."""
        retries = 0
        delay = self.initial_delay
        while retries < self.max_retries:
            try:
                self.client.login(
                    os.getenv("BLUESKY_USERNAME"),
                    os.getenv("BLUESKY_PASSWORD")
                )
                self.logger.info("Logged in successfully!")
                return
            except Exception as e:
                self.logger.error(f"Login attempt {retries + 1} failed: {e}")
                if "RateLimitExceeded" in str(e):
                    time.sleep(delay)
                    delay *= 2
                    retries += 1
                else:
                    raise e
        raise Exception("Max retries exceeded. Could not log in to Bluesky.")

    def _get_recent_posts(self) -> List[str]:
        """Fetch recent posts from the account to check for duplicates."""
        try:
            profile = self.client.get_profile(os.getenv("BLUESKY_USERNAME"))
            feed = self.client.get_author_feed(profile.did, limit=self.config['bot']['posts_to_check'])
            # Extract text from each post record
            posts = []
            for post in feed.feed:
                try:
                    if hasattr(post.record, 'text'):
                        posts.append(post.record.text.split('\n')[0])
                except AttributeError:
                    self.logger.warning(f"Unexpected post structure: {post}")
                    continue
            return posts
        except Exception as e:
            self.logger.error(f"Error fetching recent posts: {e}")
            return []

    def _is_already_posted(self, title: str) -> bool:
        """
        Check if a post with this title already exists based on configured duplicate detection settings.
        """
        try:
            # Check database if enabled
            if self.config['bot']['duplicate_detection']['check_database']:
                if self.db_handler.is_posted(title):
                    self.logger.info(f"Found post in database: {title}")
                    return True
                
            # Check recent Bluesky posts if enabled
            if self.config['bot']['duplicate_detection']['check_bluesky_backup']:
                recent_posts = self._get_recent_posts()
                if any(title.lower() in post.lower() for post in recent_posts):
                    self.logger.info(f"Found post in recent Bluesky posts: {title}")
                    # If database sync is enabled and database checking is enabled, sync the post
                    if (self.config['bot']['duplicate_detection']['auto_sync_to_database'] and 
                        self.config['bot']['duplicate_detection']['check_database']):
                        try:
                            self.db_handler.save_post(title, datetime.now().isoformat())
                            self.logger.info(f"Added missing post to database: {title}")
                        except Exception as e:
                            self.logger.error(f"Failed to save post to database: {e}")
                    return True
                
            return False
        except Exception as e:
            self.logger.error(f"Error checking if post exists: {e}")
            return True  # Err on the side of caution

    def run(self):
        """Run the bot continuously at the specified interval."""
        while True:
            try:
                self.logger.info("Fetching new RSS entries...")
                new_entries = fetch_new_rss_entries(
                    self._is_already_posted,
                    self.config['rss']['min_post_date']
                )
                
                if not new_entries:
                    self.logger.info("No new entries to post")
                else:
                    self.logger.info(f"Found {len(new_entries)} new entries to post")
                
                for entry in new_entries:
                    try:
                        self.logger.info(f"Attempting to post: {entry.title}")
                        self.post_handler.post_entry(entry)
                        
                        # Save successful posts to database if enabled
                        if self.config['bot']['duplicate_detection']['check_database']:
                            try:
                                self.db_handler.save_post(entry.title, entry.published.isoformat())
                                self.logger.info(f"Successfully saved to database: {entry.title}")
                            except Exception as e:
                                self.logger.error(f"Failed to save post to database: {e}")
                            
                        self.logger.info(f"Successfully posted: {entry.title}")
                        # Add a small delay between posts to avoid rate limits
                        time.sleep(5)
                    except Exception as e:
                        self.logger.error(f"Error posting entry {entry.title}: {e}")
                        continue

                self.logger.info(f"Sleeping for {self.interval} seconds...")
                time.sleep(self.interval)
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.logger.info(f"Sleeping for {self.interval} seconds before retrying...")
                time.sleep(self.interval)

    def __del__(self):
        """Cleanup resources when the bot is destroyed."""
        if self.db_handler:
            try:
                self.db_handler.close()
            except:
                pass
