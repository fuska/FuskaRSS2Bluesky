import time
import logging
from bot import BotLogic
from utils.logging_config import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the Bluesky RSS Posting Bot")

    bot = BotLogic()

    while True:
        try:
            logger.info("Running the bot loop")
            bot.run()
            logger.info("Bot run completed successfully. Sleeping for 10 minutes.")
        except Exception as e:
            logger.error(f"An error occurred in the main bot loop: {e}", exc_info=True)

        time.sleep(600)  # Run every 10 minutes

if __name__ == "__main__":
    main()
