# Bluesky RSS Posting Bot

This Python bot automatically posts updates from an RSS feed to your Bluesky feed. It checks the feed regularly, pulls the latest article, and creates a post with a clickable link and an optional header image. The bot also avoids duplicate posts by keeping track of previously posted articles.

## Features
- Automatically fetches and posts the latest article from the RSS feed.
- Embeds a clickable link to the article within the post.
- Retrieves and compresses the header image from the article page, posting it alongside the text.
- Prevents duplicate posts by keeping track of recently posted articles.

## Requirements
- Python 3.8+
- Libraries:
  - `requests`
  - `feedparser`
  - `beautifulsoup4`
  - `Pillow`
  - `atproto`

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local environment or preferred hosting environment:
```bash
git clone https://github.com/yourusername/bluesky-rss-posting-bot.git
cd bluesky-rss-posting-bot
```

### 2. Install Required Libraries
Install the necessary Python libraries using `pip`:
```bash
pip install requests feedparser beautifulsoup4 pillow atproto
```

### 3. Set Up Environment Variables
The bot requires your Bluesky credentials and RSS feed URL. You can provide these credentials via environment variables:

- `BLUESKY_USERNAME`: Your Bluesky username (e.g., `yourusername@bsky.social`)
- `BLUESKY_PASSWORD`: Your Bluesky password
- `RSS_FEED_URL`: The RSS feed URL to monitor for new articles

Create a `.env` file in the root directory of the project:
```env
BLUESKY_USERNAME=yourusername@bsky.social
BLUESKY_PASSWORD=yourpassword
RSS_FEED_URL=https://example.com/feed
```

### 4. Run the Bot
Once your environment is set up, run the bot using:
```bash
python main.py
```

The bot will check the RSS feed every 10 minutes for new articles and post them to Bluesky if they haven't already been posted.

### Example Post
Here’s an example of how a post might look on Bluesky:
```
Additional Funding Approved For Next Phase Of Lathrop Homes Redevelopment

Read more:
https://example.com/2024/11/xyz
```

## How It Works
1. **Fetch RSS Feed**: The bot retrieves the latest entry from the RSS feed.
2. **Duplicate Check**: It checks if the title of the latest entry has been posted before. If it has, the bot skips posting.
3. **Post Creation**:
   - **Text**: Creates a post with the article title and a clickable link to the article.
   - **Image**: If available, it retrieves the header image from the article page, compresses it to be under 1000 KB, and posts it alongside the text.
4. **Automatic Posting**: The bot posts the new article to your Bluesky feed and marks it as posted.

## Troubleshooting
- **Login Issues**: Ensure your Bluesky credentials are correct. If you encounter issues, double-check your username and password in the environment variables.
- **Image Size**: If the bot fails to post due to image size, it will skip the image and post text-only.
- **Duplicate Posts**: The bot keeps track of posted articles within each session. To maintain a history across sessions, consider implementing a persistent data store for `posted_titles`.

## Future Improvements
- **Persistent Storage**: Enhance duplicate checking by storing `posted_titles` in a database or file for persistence across sessions.
- **Multi-feed Support**: Add support for multiple RSS feeds.
- **Customizable Posting Interval**: Allow users to set the check interval.

## License
This project is open-source and available under the [MIT License](LICENSE).
