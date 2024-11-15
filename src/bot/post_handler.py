from atproto import client_utils
from utils.image_utils import download_and_compress_image
from utils.rss_parser import fetch_image_url  # Import fetch_image_url
import logging

logger = logging.getLogger(__name__)

class PostHandler:
    def __init__(self, client):
        self.client = client  # Use an existing, logged-in client instance

    def post_entry(self, entry):
        title = entry.title
        link = entry.link.rstrip('.html')

        # Create post text with a clickable link
        post_text = client_utils.TextBuilder().text(
            f"{title}\n\nRead more: "
        ).link(link, link)

        # Attempt to get image URL from the entry; if not present, fetch it from the article page
        image_url = entry.get('image_url') or fetch_image_url(link)
        if image_url:
            logger.info(f"Attempting to download and compress image: {image_url}")
            compressed_image_data = download_and_compress_image(image_url)
            if compressed_image_data:
                try:
                    logger.info("Image compression successful, attempting to send post with image")
                    # Include `image_alts` to provide alt text for accessibility
                    self.client.send_images(text=post_text, images=[compressed_image_data], image_alts=[title])
                    logger.info("Post with image sent successfully")
                except Exception as e:
                    logger.error(f"Failed to send post with image: {e}")
                    logger.info("Falling back to text-only post")
                    self.client.send_post(text=post_text)  # Fallback to text-only if image fails
            else:
                logger.warning("Image compression failed or image is too large, sending text-only post")
                self.client.send_post(text=post_text)
        else:
            logger.info("No image URL provided in entry; sending text-only post")
            self.client.send_post(text=post_text)
