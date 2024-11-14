from atproto import client_utils
from utils.image_utils import download_and_compress_image
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

        # Fetch and compress the article's header image
        image_url = entry.get('image_url')
        if image_url:
            logger.info(f"Attempting to download and compress image: {image_url}")
            compressed_image_data = download_and_compress_image(image_url)
            if compressed_image_data:
                try:
                    logger.info("Image compression successful, attempting to send post with image")
                    # Temporarily sending without `image_alts` to diagnose any potential issues with that
                    self.client.send_images(text=post_text, images=[compressed_image_data])
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
