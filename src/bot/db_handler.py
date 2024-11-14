import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '../../posts.db')

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE,
                    published_date TEXT
                )
            ''')

    def is_posted(self, title):
        """Check if the title has already been posted."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM posts WHERE title = ?", (title,))
        return cursor.fetchone() is not None

    def save_post(self, title, published_date):
        """Save a post's title and published date after posting."""
        with self.conn:
            self.conn.execute(
                "INSERT INTO posts (title, published_date) VALUES (?, ?)",
                (title, published_date)
            )

    def close(self):
        self.conn.close()
