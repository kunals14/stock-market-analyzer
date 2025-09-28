"""
Core web scraping module for collecting tweet data from Twitter/X.

This script uses Selenium to automate browser interactions, scroll through timelines,
and extract relevant data from tweets. It includes various techniques to handle
dynamic content loading, avoid bot detection, and manage data extraction efficiently.
"""

import time
import pickle
import random
import pandas as pd
from datetime import datetime, timedelta, timezone
import re
import math

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def human_like_scroll(driver):
    """Simulates a more natural, human-like scroll down the page."""
    body = driver.find_element(By.TAG_NAME, 'body')
    # Scroll a random number of times to mimic human behavior
    scrolls = math.ceil(random.uniform(2, 4))
    for _ in range(scrolls):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(random.uniform(0.5, 1.0))

def simulate_mouse_jitter(driver):
    """Simulates random mouse movements during pauses to appear less robotic."""
    try:
        actions = ActionChains(driver)
        window_size = driver.get_window_size()
        width, height = window_size.get('width'), window_size.get('height')
        for _ in range(random.randint(3, 6)):
            random_x = random.randint(int(width * 0.1), int(width * 0.9))
            random_y = random.randint(int(height * 0.1), int(height * 0.9))
            actions.move_by_offset(random_x, random_y).perform()
            time.sleep(random.uniform(0.4, 0.8))
    except Exception as e:
        print(f"Warning: Could not perform mouse jitter. Error: {e}")

def get_tweet_data(tweet_element):
    """
    Extracts all required data points from a single tweet's web element.

    Args:
        tweet_element (WebElement): The Selenium WebElement corresponding to a tweet.

    Returns:
        dict: A dictionary containing the tweet's data (username, timestamp, content,
              engagement metrics, etc.), or None if extraction fails.
    """
    try:
    # Extract a unique ID from the tweet's permalink for deduplication
        tweet_id = None
        links = tweet_element.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if href and '/status/' in href:
                tweet_id = href.split('/')[-1].split('?')[0]
                break
        if not tweet_id: return None

        username = tweet_element.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"] span').text
        timestamp_element = tweet_element.find_element(By.TAG_NAME, 'time')
        timestamp_str = timestamp_element.get_attribute('datetime')
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        content = tweet_element.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
        
        reply_count, retweet_count, like_count = 0, 0, 0
        try: reply_count = int(tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="reply"]').text)
        except (NoSuchElementException, ValueError): pass
        try: retweet_count = int(tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]').text)
        except (NoSuchElementException, ValueError): pass
        try: like_count = int(tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="like"]').text)
        except (NoSuchElementException, ValueError): pass
        
        mentions = re.findall(r'@(\w+)', content)
        hashtags = re.findall(r'#(\w+)', content)
        
        return {
            'tweet_id': tweet_id, 'username': username, 'timestamp': timestamp, 
            'content': content, 'reply_count': reply_count, 
            'retweet_count': retweet_count, 'like_count': like_count,
            'mentions': mentions, 'hashtags': hashtags
        }
    except Exception:
        return None

def scrape_twitter_data(hashtags_to_search, data_path, total_max_tweets=None, batch_size=200):
    """
    Main function to scrape tweets for a list of hashtags.

    This function iterates through each hashtag, launches a new browser session,
    logs in using saved cookies, and scrapes tweets until the target is met or
    no new tweets are found.

    Args:
        hashtags_to_search (list): A list of strings, where each is a hashtag to search.
        data_path (str): The directory path to save the output Parquet files.
        total_max_tweets (int, optional): Total number of tweets to scrape across all hashtags.
        batch_size (int, optional): Number of tweets to scrape before taking a long pause.
    """
    # ... (rest of the function)
    limit_per_hashtag = float('inf')
    if total_max_tweets and hashtags_to_search:
        limit_per_hashtag = total_max_tweets // len(hashtags_to_search)
        print(f"Total tweet target set to {total_max_tweets}. Aiming for ~{limit_per_hashtag} tweets per hashtag.")

    total_tweets_scraped = 0

    for i, hashtag in enumerate(hashtags_to_search):
        print(f"\n--- Starting scrape for #{hashtag} (Task {i+1}/{len(hashtags_to_search)}) ---")
        
        # Use standard Selenium here, as undetected_chromedriver is mainly for login
        options = webdriver.ChromeOptions()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--log-level=3') # Suppress verbose logs
        driver = webdriver.Chrome(options=options)

        try:
            # Navigate to the domain FIRST to establish context for the cookies
            driver.get("https://twitter.com/")

            # Load and filter cookies to only use those relevant to Twitter/X
            with open("twitter_cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
            for cookie in cookies:
                if 'twitter.com' in cookie.get('domain') or 'x.com' in cookie.get('domain'):
                    driver.add_cookie(cookie)
            
            # Refresh the page to apply the login session from the cookies
            print("Cookies loaded. Refreshing page to log in...")
            driver.refresh()
            time.sleep(3)
            
            search_url = f"https://twitter.com/search?q=%23{hashtag}&src=typed_query"
            driver.get(search_url)
            
            # Switch to the 'Latest' tab for chronological tweets
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Latest']]"))
            ).click()
            print("Successfully switched to 'Latest' tab.")

            all_tweet_data = []
            scraped_tweet_ids = set()
            time_limit = datetime.now(timezone.utc) - timedelta(hours=24) # Scrape tweets from the last 24 hours
            
            new_tweets_in_batch = 0
            patience = 0
            MAX_PATIENCE = 3 # How many empty scrolls to tolerate before stopping

            # Main scraping loop
            while len(scraped_tweet_ids) < limit_per_hashtag:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]')))
                tweets_on_page = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                is_past_24h_limit = False
                new_tweets_in_pass = 0
                
                for tweet_element in tweets_on_page:
                    if len(scraped_tweet_ids) >= limit_per_hashtag: break
                    tweet_data = get_tweet_data(tweet_element)
                    if tweet_data and tweet_data['tweet_id'] not in scraped_tweet_ids:
                        if tweet_data['timestamp'] >= time_limit:
                            all_tweet_data.append(tweet_data)
                            scraped_tweet_ids.add(tweet_data['tweet_id'])
                            new_tweets_in_batch += 1
                            new_tweets_in_pass += 1
                        else:
                            is_past_24h_limit = True
                            break
                
                if is_past_24h_limit:
                    print("Found tweets older than 24 hours. Concluding scrape for this hashtag.")
                    break
                
                # If no new tweets are found after several scrolls, assume end of feed
                if new_tweets_in_pass == 0:
                    patience += 1
                    print(f"No new tweets found in this scroll pass. Patience: {patience}/{MAX_PATIENCE}")
                    if patience >= MAX_PATIENCE:
                        print("Reached max patience. Assuming end of feed for this session.")
                        break
                else:
                    patience = 0 # Reset patience if new tweets were found

                # Take a long pause after scraping a batch to mimic human behavior
                if new_tweets_in_batch >= batch_size:
                    pause_duration = random.uniform(60, 120)
                    print(f"Batch of {new_tweets_in_batch} tweets completed. Pausing for {pause_duration/60:.2f} minutes...")
                    simulate_mouse_jitter(driver)
                    time.sleep(pause_duration)
                    new_tweets_in_batch = 0
                    print("Resuming scrape.")
                
                human_like_scroll(driver)
                time.sleep(random.uniform(2, 4))
            
            if all_tweet_data:
                df = pd.DataFrame(all_tweet_data)
                df.drop_duplicates(subset=['tweet_id'], inplace=True)
                # Save data in the preferred Parquet format for efficiency
                output_file = f"{data_path}/{hashtag}_tweets.parquet"
                df.to_parquet(output_file, index=False)
                print(f"Saved {len(df)} unique tweets for #{hashtag} to {output_file}")
                total_tweets_scraped += len(df)
        
        except TimeoutException:
            print(f"WARNING: A timeout occurred while scraping #{hashtag}. Moving on.")
        finally:
            driver.quit()
        
        # Wait between scraping different hashtags
        if i < len(hashtags_to_search) - 1:
            delay = random.uniform(15, 30)
            print(f"Waiting for {delay:.0f} seconds before starting next hashtag...")
            time.sleep(delay)

    print("\nAll scraping tasks completed.")
    print("\n--- SCRAPING SUMMARY ---")
    print(f"Total unique tweets processed across all hashtags: {total_tweets_scraped}")