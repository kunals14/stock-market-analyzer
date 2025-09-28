"""
Main execution script for the Twitter/X scraping and analysis pipeline.

This script orchestrates the entire process:
1. It checks for valid login cookies.
2. It runs the web scraper to collect raw tweet data.
3. It runs the data processor to clean the raw data.
4. It logs the total execution time.
"""

import os
import time
from datetime import timedelta

from src.cookie_handler import are_cookies_valid, generate_new_cookies
from src.data_processor import process_raw_data
from src.scraper import scrape_twitter_data

if __name__ == "__main__":
    # --- Core Configuration ---
    HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]
    TOTAL_TWEETS_TARGET = 200
    BATCH_SIZE = 50
    
    # --- Path Configuration ---
    RAW_DATA_PATH = "data/raw_tweets"
    PROCESSED_DATA_PATH = "data/processed_tweets" # <-- NEW PATH
    
    # --- Pipeline Configuration ---
    COOKIE_FILE = "twitter_cookies.pkl"
    COOKIE_MAX_AGE_DAYS = 7

    start_time = time.perf_counter()
    
    # --- Step 1: Automated Cookie Management ---
    if not are_cookies_valid(COOKIE_FILE, COOKIE_MAX_AGE_DAYS):
        generate_new_cookies(COOKIE_FILE)

    # --- Step 2: Run the Scraper ---
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    print("\nStarting the tweet scraping process...")
    scrape_twitter_data(
        hashtags_to_search=HASHTAGS,
        data_path=RAW_DATA_PATH,
        total_max_tweets=TOTAL_TWEETS_TARGET,
        batch_size=BATCH_SIZE
    )

    # --- Step 3: Clean and Process Raw Data ---
    process_raw_data(
        raw_dir=RAW_DATA_PATH,
        processed_dir=PROCESSED_DATA_PATH
    )
    
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    elapsed_td = timedelta(seconds=elapsed)

    print(f"\nTotal elapsed time: {elapsed:.2f} seconds ({str(elapsed_td)})")