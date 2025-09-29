"""
Performs analysis on cleaned tweet data to generate quantitative trading signals.
"""

import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def load_processed_data(processed_dir):
    print("\n--- Loading Processed Data for Analysis ---")
    processed_files = glob.glob(os.path.join(processed_dir, "*.parquet"))
    if not processed_files:
        print("No processed data files found.")
        return None
    df_list = [pd.read_parquet(file) for file in processed_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
    combined_df.sort_values(by='timestamp', inplace=True)
    print(f"Loaded and combined {len(combined_df)} tweets from {len(processed_files)} files.")
    return combined_df

def calculate_polarity(text, positive_words, negative_words):
    if not isinstance(text, str):
        return 0
    words = text.split()
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    return positive_score - negative_score

def generate_trading_signal(df):
    print("Generating trading signals using sentiment polarity...")
    positive_words = set(['bullish', 'profit', 'up', 'rally', 'booming', 'gain', 'surge', 'breakout', 'buy', 'long', 'strong', 'uptrend', 'boom', 'bull', 'growth', 'teji', 'munafa', 'badhat', 'kharido', 'तेजी', 'मुनाफा', 'बढ़त', 'खरीदें'])
    negative_words = set(['bearish', 'loss', 'down', 'crash', 'slump', 'decline', 'dip', 'selloff', 'sell', 'short', 'weak', 'falling', 'downtrend', 'bear', 'panic', 'mandi', 'giravat', 'nuksan', 'becho', 'मंदी', 'गिरावट', 'नुकसान', 'बेचें'])
    df['trading_signal'] = df['cleaned_content'].apply(lambda text: calculate_polarity(text, positive_words, negative_words))
    print("Base trading signal generation complete.")
    return df

def aggregate_signals(df):
    """
    Combines text-based signals with other features to create a composite signal.
    """
    print("Aggregating signals to create a composite score...")

    df['engagement_score'] = np.log1p(df['reply_count'] + df['retweet_count'] + df['like_count'])

    scaler = MinMaxScaler()
    df[['signal_norm', 'engagement_norm']] = scaler.fit_transform(df[['trading_signal', 'engagement_score']])
    
    df['composite_signal'] = (0.6 * df['signal_norm']) + (0.4 * df['engagement_norm'])
    
    df['confidence'] = df['engagement_norm']
    
    print("Signal aggregation complete.")
    return df

def create_sentiment_visualization(df, output_dir):
    print("Creating sentiment visualization...")
    if df.empty:
        print("DataFrame is empty, skipping visualization.")
        return

    df.set_index('timestamp', inplace=True)
    
    hourly_sentiment = df['composite_signal'].resample('1H').mean()
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(15, 7))
    hourly_sentiment.plot(kind='line', ax=ax, color='cyan', marker='o', label='Hourly Avg. Composite Signal')
    
    ax.set_title('Hourly Average Market Sentiment Signal (Last 24 Hours)', fontsize=16)
    ax.set_ylabel('Average Composite Signal', fontsize=12)
    ax.set_xlabel('Time (UTC)', fontsize=12)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, "sentiment_over_time.png")
    fig.savefig(output_path)
    
    print(f"Sentiment visualization saved to '{output_path}'")
    df.reset_index(inplace=True)