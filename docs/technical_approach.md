# Technical Approach Documentation

This document explains the technical strategies used to build a robust and efficient market intelligence system.

### 1. Data Collection Strategy

The system uses the **Selenium** library to perform automated web scraping. This approach directly interacts with the Twitter/X website, simulating real user behavior to navigate and extract data dynamically.

### 2. Anti-Bot Evasion and Rate Limiting

A multi-layered strategy was designed to avoid bot detection:

-   **Hybrid Browser Approach**: The system uses `undetected-chromedriver` for the initial, one-time manual login. This specialized browser is patched to avoid detection during the sensitive login phase. For subsequent scraping tasks, it switches to a standard `webdriver.Chrome` instance, which is less resource-intensive.
-   **Session Persistence via Cookies**: Instead of logging in with credentials on every run, the system saves the session cookies after the first manual login. Future runs load these cookies to instantly gain authenticated access, bypassing login forms and 2FA challenges entirely.
-   **Human Behavior Simulation**: To appear less robotic, the scraper incorporates several human-like actions:
    -   **Browser Warm-up**: The cookie generation process first visits a neutral site (`google.com`) before navigating to Twitter/X.
    -   **Randomized Pauses**: The script implements long, random pauses between scraping batches and shorter pauses between scrolls to mimic human reading time.
    -   **Natural Scrolling**: The scraper scrolls down the page in smaller, randomized increments (`PAGE_DOWN`) instead of a single, programmatic scroll to the bottom.
    -   **Mouse Jitter**: During long pauses, the script simulates random mouse movements on the screen.

### 3. Data Processing and Storage

-   **Storage Format**: Data is stored in the **Parquet format** as required. This columnar format offers high compression and is highly efficient for the type of analytical queries performed in this project.
-   **Unicode Handling**: The text cleaning function (`clean_tweet_text`) uses a specific regex pattern `[^\w\s\u0900-\u097F]` to remove special characters while preserving alphanumeric characters and the Devanagari script, ensuring that content in Indian languages is handled correctly.
-   **Deduplication**: To ensure data integrity, a robust deduplication mechanism is used. The unique ID of each tweet is extracted and stored in a Python `set`. This provides a highly efficient O(1) average time complexity for checking if a tweet has already been collected, preventing any duplicates in the final dataset.

### 4. Analysis and Signal Generation

-   **Text-to-Signal Conversion**: The system uses a lexicon-based sentiment analysis approach. A predefined list of positive and negative keywords (including common terms in English and Hindi) is used to calculate a `trading_signal` score for each tweet (Positive Words - Negative Words).
-   **Signal Aggregation**: The raw `trading_signal` is combined with a log-transformed `engagement_score` (replies + retweets + likes) to create a `composite_signal`. This approach gives more weight to tweets that are not only positive or negative but also have high visibility and engagement.
-   **Confidence Score**: The normalized engagement score is used as a proxy for the `confidence` of the signal, operating on the assumption that a signal from a highly engaged tweet is more reliable.