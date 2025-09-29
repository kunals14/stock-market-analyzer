"""
Main execution script for the Twitter/X scraping and analysis pipeline.

This script can be run in two modes:
1. Full Pipeline (default): Runs the entire process from scraping to analysis.
   - Usage: python main.py

2. Analysis Only: Skips scraping and processing, and runs only the analysis
   on existing processed data.
   - Usage: python main.py --skip-scraping
"""

import os
import time
import pandas as pd
import argparse
from datetime import timedelta
from src.scraper import scrape_twitter_data
from src.cookie_handler import are_cookies_valid, generate_new_cookies
from src.data_processor import process_raw_data
from src.analysis_engine import load_processed_data, generate_trading_signal, aggregate_signals, create_sentiment_visualization

if __name__ == "__main__":
    # --- Add a command-line argument parser ---
    parser = argparse.ArgumentParser(description="Run the Twitter Market Intelligence Pipeline.")
    parser.add_argument(
        '--skip-scraping',
        action='store_true',
        help="Skip scraping and processing, and run only the analysis step."
    )
    args = parser.parse_args()
    
    # --- Configuration ---
    HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]
    TOTAL_TWEETS_TARGET = 2000
    BATCH_SIZE = 200
    RAW_DATA_PATH = "data/raw_tweets"
    PROCESSED_DATA_PATH = "data/processed_tweets"
    ANALYSIS_OUTPUT_PATH = "data/analysis_results"
    COOKIE_FILE = "twitter_cookies.pkl"
    COOKIE_MAX_AGE_DAYS = 7
    start_time = time.perf_counter()

    # --- Conditionally run scraping and processing ---
    if not args.skip_scraping:
        # --- Step 1: Automated Cookie Management ---
        if not are_cookies_valid(COOKIE_FILE, COOKIE_MAX_AGE_DAYS):
            generate_new_cookies(COOKIE_FILE)

        # --- Step 2: Run the Scraper ---
        os.makedirs(RAW_DATA_PATH, exist_ok=True)
        print("\n--- Starting SCRAPING phase ---")
        scrape_twitter_data(hashtags_to_search=HASHTAGS, data_path=RAW_DATA_PATH, total_max_tweets=TOTAL_TWEETS_TARGET, batch_size=BATCH_SIZE)

        # --- Step 3: Clean and Process Raw Data ---
        print("\n--- Starting PROCESSING phase ---")
        process_raw_data(raw_dir=RAW_DATA_PATH, processed_dir=PROCESSED_DATA_PATH)
    else:
        print("\n--- Skipping SCRAPING and PROCESSING phases ---")

    # --- Step 4: Full Analysis Pipeline (This will always run) ---
    print("\n--- Starting ANALYSIS phase ---")
    processed_df = load_processed_data(PROCESSED_DATA_PATH)
    if processed_df is not None and not processed_df.empty:
        signal_df = generate_trading_signal(processed_df)
        final_df = aggregate_signals(signal_df)
        
        os.makedirs(ANALYSIS_OUTPUT_PATH, exist_ok=True)
        create_sentiment_visualization(final_df, ANALYSIS_OUTPUT_PATH)
        
        output_file = os.path.join(ANALYSIS_OUTPUT_PATH, "trading_signals.parquet")
        final_df.to_parquet(output_file, index=False)
        
        print(f"\nAnalysis complete. Final data saved to '{output_file}'")
        print("\n--- Sample of Final Data with Composite Signal ---")
        print(final_df[['timestamp', 'cleaned_content', 'trading_signal', 'composite_signal', 'confidence']].tail())

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    elapsed_td = timedelta(seconds=elapsed)
    print(f"\nTotal elapsed time: {elapsed:.2f} seconds ({str(elapsed_td)})")