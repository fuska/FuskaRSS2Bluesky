# Bluesky RSS Posting Bot

This Python bot automatically posts updates from an RSS feed to your Bluesky feed. It checks the feed regularly, retrieves new articles, and creates posts with clickable links and optional header images. The bot uses a database to avoid duplicate posts by tracking previously posted articles, even across sessions.

## Features
- Automatically fetches and posts new articles from the RSS feed
- Creates formatted posts with clickable links to articles
- Smart image handling:
  - Automatically retrieves header images from article pages
  - Compresses images to meet Bluesky's size requirements
  - Falls back to text-only posts if image processing fails
- Robust duplicate prevention:
  - Uses SQLite database to track all posted articles
  - Double-checks against recent Bluesky posts as backup
  - Automatically syncs missing posts to database
- Reliable operation:
  - Implements exponential backoff for login attempts
  - Handles rate limits automatically
  - Includes comprehensive error handling and logging
- Highly configurable through YAML:
  - Customizable check intervals
  - Adjustable retry settings
  - Configurable logging levels
  - Minimum post date filtering

## Requirements
- Python 3.8+
- Libraries:
  - `requests`
  - `feedparser`
  - `beautifulsoup4`
  - `Pillow`
  - `atproto`
  - `python-dotenv`
  - `pyyaml`

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local environment or preferred hosting environment:

```bash
git clone https://github.com/MisterClean/ChicagoYIMBYblueskybot.git
cd bluesky-rss-posting-bot
```

### 2. Install Required Libraries
Install the necessary Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory with your credentials:

```env
BLUESKY_USERNAME=yourusername@bsky.social
BLUESKY_PASSWORD=yourpassword
RSS_FEED_URL=https://example.com/feed
```

### 4. Configure Settings (Optional)
The bot uses a `config.yaml` file for customizable settings:
- Check interval for new posts
- Maximum retry attempts
- Initial delay between retries
- Logging level and format
- Minimum post date filter
- Number of recent posts to check for duplicates

### 5. Run the Bot
Start the bot using:

```bash
python src/main.py
```

## How It Works

### Post Creation Process
1. **RSS Fetching**: Regularly checks the RSS feed for new articles
2. **Duplicate Detection**:
   - Checks SQLite database for previously posted articles
   - Verifies against recent Bluesky posts as a backup
   - Automatically syncs any posts found on Bluesky but missing from database
3. **Image Processing**:
   - Attempts to extract header image from article
   - Compresses image to meet Bluesky's size limits
   - Gracefully falls back to text-only if image processing fails
4. **Post Formatting**:
   - Creates formatted post with article title
   - Adds clickable link to article
   - Attaches processed image if available
5. **Error Handling**:
   - Implements exponential backoff for login attempts
   - Handles rate limits automatically
   - Logs all operations for debugging

### Post Format Example
```
Article Title

Read more: https://example.com/article-link
[Attached Image]
```

## Reliability Features

### Error Handling
- Exponential backoff for login attempts
- Automatic retry on rate limits
- Graceful fallbacks for image processing
- Comprehensive logging for debugging

### Duplicate Prevention
- Primary check against SQLite database
- Secondary check against recent Bluesky posts
- Automatic database synchronization
- Configurable number of posts to check

### Rate Limit Management
- Built-in delays between posts
- Automatic handling of API rate limits
- Configurable retry settings

## Troubleshooting

### Common Issues
- **Login Failures**: The bot will automatically retry with exponential backoff
- **Image Processing**: Falls back to text-only posts if image processing fails
- **Database Sync**: Automatically repairs database if posts are found on Bluesky but missing from local storage
- **Rate Limits**: Handled automatically with configurable delays

### Logging
- Configurable logging levels in `config.yaml`
- Detailed error messages for debugging
- Operation tracking for monitoring

## License
This project is open-source and available under the [MIT License](LICENSE).
