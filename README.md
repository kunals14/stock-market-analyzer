# Real-Time Market Intelligence System for Indian Stocks

## 1. Overview

This project is a complete data pipeline that scrapes, processes, analyzes, and visualizes discussions about the Indian stock market from Twitter/X. It is designed to operate without paid APIs, using creative web scraping techniques to gather real-time data for generating quantitative trading signals.

## 2. Core Features

-   **Automated Data Collection**: Scrapes tweets using specific hashtags like `#nifty50` and `#sensex` from the last 24 hours.
-   **Smart Anti-Bot Evasion**: Bypasses bot detection using a sophisticated session management system. It requires a one-time manual login to generate session cookies, which are then used for all future automated scraping runs.
-   **Comprehensive Data Extraction**: Captures key data points including username, timestamp, tweet content, engagement metrics (likes, replies, retweets), mentions, and hashtags.
-   **Efficient Data Processing**: Cleans and normalizes raw text data, with specific support for Unicode characters found in Indian languages.
-   **Quantitative Signal Generation**: Converts cleaned text into a numerical `trading_signal` based on sentiment polarity. This signal is then combined with engagement metrics to create a weighted `composite_signal`.
-   **Optimized Storage**: Saves all data in the columnar **Parquet** format for efficient storage and fast analytical queries.
-   **Data Visualization**: Generates a plot showing the hourly average market sentiment over time, providing a clear visual summary of the analysis.

## 3. Project Structure

```
stock-market-analyzer/
│
├── data/
│   ├── raw_tweets/         # Stores raw scraped data
│   ├── processed_tweets/   # Stores cleaned data
│   └── analysis_results/   # Stores final signals and visualizations
│
├── docs/
│   ├── technical_approach.md
│   └── data_schema.md
│
├── src/
│   ├── init.py
│   ├── cookie_handler.py     # Manages session cookies
│   ├── data_processor.py     # Cleans raw data
│   ├── scraper.py            # Scrapes Twitter/X
│   └── analysis_engine.py    # Generates signals and insights
│
├── .gitignore
├── main.py                 # Main execution script
├── requirements.txt        # Project dependencies
└── README.md
```

## 4. Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd stock-market-analyzer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 5. How to Run

You can run the entire pipeline or just the analysis part on existing data.

### Full Pipeline (Scrape, Process, and Analyze)

Execute the main script from the root directory:
```bash 
python main.py
```
-   **First Run:** On the first run, or if the session cookies are older than 7 days, a browser window will open. You will be prompted to log in to your Twitter/X account manually. After you are logged in, return to the terminal without closing the browser and press Enter. This saves your session cookies for future runs.
-   **Subsequent Runs:** The script will use the saved cookies to log in automatically and begin scraping.

## Analysis Only
If you have already scraped and processed the data, you can run only the analysis step:

```bash
python main.py --skip-scraping
```
This will use the data in data/processed_tweets/ to generate the final output in data/analysis_results/.