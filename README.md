# Real-Time Market Intelligence System for Indian Stock Markets

## 1. Overview

This project is a data collection and analysis system designed to gather real-time market intelligence from Twitter/X discussions related to the Indian stock market. It systematically scrapes, processes, and stores tweets containing relevant hashtags, laying the groundwork for quantitative signal analysis for algorithmic trading (see `docs/technical_approach.md`). This system is built to be robust, handling anti-bot measures creatively and ensuring data integrity.

## 2. Features

**Automated Tweet Scraping:** Collects tweets from Twitter/X for specified hashtags (`#nifty50`, `#sensex`, etc.) from the last 24 hours (see `docs/technical_approach.md`).
**Comprehensive Data Extraction:** Gathers key data points including username, timestamp, content, engagement metrics (replies, retweets, likes), mentions, and hashtags (see `docs/data_schema.md`).
**Anti-Bot Evasion:** Implements a sophisticated, multi-layered strategy to handle rate limiting and anti-bot measures without using paid APIs (see `docs/technical_approach.md`).
- **Session Persistence:** Uses a cookie-based system to maintain login sessions, minimizing the need for manual intervention.
**Efficient Storage:** Saves cleaned data in the efficient, columnar Parquet format as described in `docs/data_schema.md`.
**Data Integrity:** Ensures data is unique through a robust deduplication mechanism based on tweet IDs (see `src/scraper.py`).
**Production-Ready Code:** The codebase is documented with comments and docstrings and includes error handling (see `src/`).

## 3. Project Structure

```
stock-market-analyzer/
│
├── data/
│   ├── raw_tweets/
│   ├── processed_tweets/
│   └── analysis_results/
│
├── docs/
│   ├── technical_approach.md
│   └── data_schema.md
│
├── src/
│   ├── __init__.py
│   ├── cookie_handler.py
│   ├── data_processor.py
│   ├── scraper.py
│   └── analysis_engine.py
│
├── venv/
│
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## 4. Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd QuantTweet
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

Execute the main script from the root directory:

```bash
python main.py
```
-   **First Run:** On the first run, or if the session cookies are older than 7 days, a browser window will open. You will be prompted to log in to your Twitter/X account manually. After you log in, press `Enter` in the terminal.
-   **Subsequent Runs:** The script will use the saved cookies to log in automatically and begin scraping.

The collected data will be saved as `.parquet` files in the `data/raw_tweets/` directory.