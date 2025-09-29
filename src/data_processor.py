"""
Processes raw tweet data from Parquet files into a cleaned format.

This module reads raw data collected by the scraper, applies various text cleaning
and normalization techniques to the tweet content, and saves the cleaned data
to a new location, preparing it for analysis.
"""

import pandas as pd
import re
import os
import glob

def clean_tweet_text(text):
    """
    Applies a series of cleaning steps to a single string of tweet text.

    Args:
        text (str): The raw text content of a tweet.

    Returns:
        str: The cleaned and normalized text.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # 3. Remove user mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # 4. Remove the hash symbol from hashtags, but keep the text
    text = text.replace('#', '')
    
    # 5. Remove special characters, punctuation, and emojis
    # This regex keeps alphanumeric characters and essential Indian 
    # language characters (Devanagari) to handle unicode content.
    text = re.sub(r'[^\w\s\u0900-\u097F]', '', text)
    
    # 6. Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def process_raw_data(raw_dir, processed_dir):
    """
    Finds all raw Parquet files, cleans them, and saves to a new directory.

    Args:
        raw_dir (str): The directory containing the raw tweet Parquet files.
        processed_dir (str): The directory where cleaned Parquet files will be saved.
    """
    print("\n--- Starting Data Cleaning and Processing ---")
    
    # Ensure the output directory exists
    os.makedirs(processed_dir, exist_ok=True)
    
    # Find all Parquet files in the raw data directory
    raw_files = glob.glob(os.path.join(raw_dir, "*.parquet"))
    
    if not raw_files:
        print("No raw data files found to process.")
        return

    total_files = len(raw_files)
    print(f"Found {total_files} raw data file(s) to process.")
    
    for i, file_path in enumerate(raw_files):
        filename = os.path.basename(file_path)
        print(f"Processing file {i+1}/{total_files}: {filename}...")
        
        try:
            # Read the raw data
            df = pd.read_parquet(file_path)
            
            # Apply the cleaning function to the 'content' column
            df['cleaned_content'] = df['content'].apply(clean_tweet_text)
            
            # Select and reorder columns for the final output
            output_columns = [
                'tweet_id', 'timestamp', 'username', 'content', 'cleaned_content',
                'reply_count', 'retweet_count', 'like_count', 'mentions', 'hashtags'
            ]
            df = df[output_columns]
            
            # Save the cleaned DataFrame to the processed directory
            output_path = os.path.join(processed_dir, filename)
            df.to_parquet(output_path, index=False)
            
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            
    print("\nData cleaning and processing complete.")
    print(f"Cleaned files are saved in '{processed_dir}'")