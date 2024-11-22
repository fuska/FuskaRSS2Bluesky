# Bluesky RSS Posting Bot

This Python bot automatically posts updates from an RSS feed to your Bluesky feed. It checks the feed regularly, retrieves new articles, and creates posts with clickable links and optional header images. The bot uses a database to avoid duplicate posts by tracking previously posted articles, even across sessions.

## Features
- Automatically fetches and posts new articles from the RSS feed
- Creates formatted posts with clickable links to articles
- Smart image handling:
  - Configurable image posting (can be enabled/disabled)
  - Configurable image source priorities (og:image, twitter:image, etc.)
  - Automatically retrieves header images from article pages
  - Compresses images to meet Bluesky's size requirements
  - Falls back to text-only posts if image processing fails
- Robust duplicate prevention:
  - Configurable duplicate detection strategies
  - Optional database tracking of posted articles
  - Optional backup check against recent Bluesky posts
  - Configurable automatic database synchronization
- Reliable operation:
  - Implements exponential backoff for login attempts
  - Handles rate limits automatically
  - Includes comprehensive error handling and logging
- Highly configurable through YAML:
  - Customizable post format
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

### 4. Configure Settings
The bot uses a `config.yaml` file for extensive customization. Here's a comprehensive example with all available options:

```yaml
# RSS Feed Configuration
rss:
  min_post_date: "2024-11-13"  # Format: YYYY-MM-DD
  image_sources:  # Order determines priority
    use_og_image: true         # Use OpenGraph image meta tag
    use_twitter_image: true    # Use Twitter card image meta tag
    use_wp_post_image: true    # Use WordPress featured image
    use_first_image: true      # Fallback to first img tag found

# Bot Settings
bot:
  check_interval: 600  # seconds
  max_retries: 5
  initial_delay: 10
  posts_to_check: 50
  include_images: true  # Master switch for image posting
  post_format: "{title}\n\nRead more: {link}"  # Supports {title} and {link} placeholders
  duplicate_detection:
    check_database: true        # Use SQLite database for duplicate checking
    check_bluesky_backup: true  # Backup check against recent posts
    auto_sync_to_database: true # Auto-sync posts found on Bluesky to database

# Logging
logging:
  level: INFO
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

#### Configuration Options Explained

##### RSS Settings
- `min_post_date`: Minimum date for posts to be considered
- `image_sources`: Configure which image sources to try and in what order
  - `use_og_image`: Try OpenGraph meta tags
  - `use_twitter_image`: Try Twitter card meta tags
  - `use_wp_post_image`: Try WordPress featured image
  - `use_first_image`: Fall back to first image found in page

##### Bot Settings
- `check_interval`: Time between RSS feed checks in seconds
- `max_retries`: Maximum login retry attempts
- `initial_delay`: Initial delay between retries
- `posts_to_check`: Number of recent posts to check for duplicates
- `include_images`: Master switch to enable/disable image posting
- `post_format`: Template for post text (supports {title} and {link} placeholders)
- `duplicate_detection`: Configure duplicate post detection strategy
  - `check_database`: Enable/disable database checking
  - `check_bluesky_backup`: Enable/disable checking recent Bluesky posts
  - `auto_sync_to_database`: Enable/disable automatic database synchronization

##### Logging Settings
- `level`: Logging level (INFO, DEBUG, WARNING, ERROR)
- `format`: Log message format

### 5. Run the Bot
Start the bot using:

```bash
python src/main.py
```

## How It Works

### Post Creation Process
1. **RSS Fetching**: Regularly checks the RSS feed for new articles
2. **Duplicate Detection** (configurable):
   - Checks SQLite database if enabled
   - Verifies against recent Bluesky posts if enabled
   - Optionally syncs posts found on Bluesky to database
3. **Image Processing** (if enabled):
   - Attempts to extract header image using configured sources
   - Compresses image to meet Bluesky's size limits
   - Gracefully falls back to text-only if image processing fails
4. **Post Formatting**:
   - Creates formatted post using configured template
   - Adds clickable link to article
   - Attaches processed image if available and enabled
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
- Configurable primary database check
- Optional backup check against recent posts
- Optional automatic database synchronization
- Configurable number of posts to check

### Rate Limit Management
- Built-in delays between posts
- Automatic handling of API rate limits
- Configurable retry settings

## Troubleshooting

### Common Issues
- **Login Failures**: The bot will automatically retry with exponential backoff
- **Image Processing**: Falls back to text-only posts if image processing fails
- **Database Sync**: Optionally repairs database if posts are found on Bluesky but missing from local storage
- **Rate Limits**: Handled automatically with configurable delays

### Logging
- Configurable logging levels in `config.yaml`
- Detailed error messages for debugging
- Operation tracking for monitoring

## License
This project is open-source and available under the [MIT License](LICENSE).
