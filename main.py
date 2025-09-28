"""
Main execution script for the Twitter/X scraping and analysis pipeline.

This script orchestrates the entire process:
1. It checks for valid login cookies and initiates a new login if they are
   missing or expired.
2. It runs the web scraper to collect tweet data based on specified hashtags.
3. It logs the total execution time.
"""

import os
import time
from datetime import timedelta
from src.scraper import scrape_twitter_data
from src.cookie_handler import are_cookies_valid, generate_new_cookies

if __name__ == "__main__":
    # --- Core Configuration ---
    # Hashtags to search for, as required by the assignment [cite: 10]
    HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]
    # Total number of unique tweets to aim for across all hashtags [cite: 12]
    TOTAL_TWEETS_TARGET = 2000
    # The scraper will pause after collecting this many tweets for a single hashtag
    BATCH_SIZE = 200
    # Directory to save the output Parquet files
    OUTPUT_DATA_PATH = "data/raw_tweets"

    # --- Pipeline Configuration ---
    # Filename for storing login session cookies
    COOKIE_FILE = "twitter_cookies.pkl"
    # Maximum age of cookies in days before requiring a new login
    COOKIE_MAX_AGE_DAYS = 7

    # --- Step 1: Automated Cookie Management ---
    # Check if cookies are valid or need to be created/refreshed.
    if not are_cookies_valid(COOKIE_FILE, COOKIE_MAX_AGE_DAYS):
        generate_new_cookies(COOKIE_FILE)

    # Ensure the output directory for data exists
    os.makedirs(OUTPUT_DATA_PATH, exist_ok=True)

    # --- Step 2: Run the Scraper ---
    print("\nStarting the tweet scraping process...")
    start_time = time.perf_counter()

    scrape_twitter_data(
        hashtags_to_search=HASHTAGS,
        data_path=OUTPUT_DATA_PATH,
        total_max_tweets=TOTAL_TWEETS_TARGET,
        batch_size=BATCH_SIZE
    )

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    elapsed_td = timedelta(seconds=elapsed)

    print(f"\nTotal elapsed time: {elapsed:.2f} seconds ({str(elapsed_td)})")