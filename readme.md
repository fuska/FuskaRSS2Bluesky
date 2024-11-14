# Bluesky RSS Posting Bot

This Python bot automatically posts updates from an RSS feed to your Bluesky feed. It checks the feed regularly, retrieves new articles, and creates posts with clickable links and optional header images. The bot uses a database to avoid duplicate posts by tracking previously posted articles, even across sessions.

## Features
- Automatically fetches and posts new articles from the RSS feed.
- Embeds clickable links to the articles within each post.
- Retrieves and compresses the header image from the article page, posting it alongside the text.
- Prevents duplicate posts by keeping track of posted articles in a persistent SQLite database.
- Configurable to support any RSS feed URL, allowing for easy customization.

## Requirements
- Python 3.8+
- Libraries:
  - `requests`
  - `feedparser`
  - `beautifulsoup4`
  - `Pillow`
  - `atproto`
  - `dotenv`

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
The bot requires your Bluesky credentials and the RSS feed URL to monitor. You can provide these via environment variables:

- `BLUESKY_USERNAME`: Your Bluesky username (e.g., `yourusername@bsky.social`)
- `BLUESKY_PASSWORD`: Your Bluesky password
- `RSS_FEED_URL`: The RSS feed URL to monitor for new articles

Create a `.env` file in the root directory of the project with the following content:

```env
BLUESKY_USERNAME=yourusername@bsky.social
BLUESKY_PASSWORD=yourpassword
RSS_FEED_URL=https://example.com/feed
```

### 4. Run the Bot
Once your environment is set up, run the bot using:

```bash
python src/main.py
```

The bot will check the RSS feed every 10 minutes for new articles and post them to Bluesky if they haven’t already been posted.

### Example Post
Here’s an example of how a post might look on Bluesky:

```
Additional Funding Approved For Next Phase Of Lathrop Homes Redevelopment

Read more:
https://example.com/2024/11/xyz
```

## How It Works
1. **Fetch RSS Feed**: The bot retrieves the latest articles from the RSS feed.
2. **Duplicate Check**: It checks each article title against the entries in the SQLite database. If the article has already been posted, it skips posting.
3. **Post Creation**:
   - **Text**: Creates a post with the article title and a clickable link to the article.
   - **Image**: If available, it retrieves the header image from the article page, compresses it to be under 1000 KB, and posts it alongside the text.
4. **Automatic Posting**: The bot posts new articles to your Bluesky feed and records them in the database to prevent reposting.

## Using This Bot for Your Own RSS Feed

To use this bot with your own RSS feed:
1. Set the `RSS_FEED_URL` in the `.env` file to your desired feed URL.
2. Update `BLUESKY_USERNAME` and `BLUESKY_PASSWORD` with your own Bluesky credentials.
3. Run the bot using `python src/main.py`. The bot will continuously monitor the feed and post new articles as they are published.

## Troubleshooting
- **Login Issues**: Ensure your Bluesky credentials are correct. If you encounter issues, double-check your username and password in the `.env` file.
- **Image Size**: If the bot fails to post due to image size, it will skip the image and post text-only.
- **Duplicate Posts**: The bot uses an SQLite database (`posts.db`) to track posted articles, ensuring duplicates are avoided across sessions.

## Future Improvements
- **Multi-feed Support**: Add support for multiple RSS feeds.
- **Customizable Posting Interval**: Allow users to set the check interval.
- **Enhanced Error Handling**: Improve error handling for network issues or feed parsing errors.

## License
This project is open-source and available under the [MIT License](LICENSE).
