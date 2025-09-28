# Technical Approach Documentation

This document outlines the technical decisions and strategies implemented in the data collection pipeline.

### 1. Data Collection Method

To meet the constraint of not using any paid APIs, this system uses **web scraping** via the **Selenium** library. This approach allows for direct interaction with the Twitter/X web interface, mimicking user behavior to navigate and extract data.

### 2. Anti-Bot Evasion Strategy

A multi-layered strategy was designed to handle and evade bot detection mechanisms:

-   **`undetected-chromedriver`:** The initial login and cookie generation process is handled by `undetected-chromedriver`, a specialized library patched to prevent detection by common bot-blocking services.
-   **Session Persistence via Cookies:** Instead of logging in with credentials every time, the system logs in manually once and saves the session cookies. Subsequent runs load these cookies into a standard Selenium browser, which is a less detectable and more efficient method for authenticated scraping.
-   **Human-like Behavior Simulation:**
    -   **Browser Warm-up:** The cookie generation process starts by visiting a neutral site (`google.com`) before navigating to Twitter, which is a more natural browsing pattern.
    -   **Randomized Pauses:** The scraper takes long, randomized pauses between scraping batches and shorter pauses between scrolls to mimic human reading and interaction times.
    -   **Human-like Scrolling:** The script scrolls down the page in randomized, page-down increments rather than executing a single large scroll.
    -   **Mouse Jitter:** During long pauses, the script simulates random mouse movements.

### 3. Data Storage and Schema

-   **Storage Format:** Data is stored in the **Parquet format** as requested. Parquet was chosen for its high compression ratios and efficient columnar storage, which is ideal for analytical queries and handling large datasets.
-   **Schema:** The data schema is designed to be flat and efficient. Please see `data_schema.md` for a detailed breakdown of the columns.

### 4. Data Deduplication

To ensure data integrity, a **deduplication mechanism** is implemented before saving the data. Each tweet's unique ID is extracted from its permalink. This ID is stored in a Python `set` for fast, O(1) average time complexity lookups. If a tweet ID has already been seen, it is discarded, guaranteeing that the final dataset contains no duplicate entries.