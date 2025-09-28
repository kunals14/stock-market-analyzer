# Data Schema

The data collected by the scraper is stored in Parquet files, with one file per hashtag scraped. The schema for these files is as follows, designed to capture all required data points.

| Column Name     | Data Type          | Description                                                                 |
|-----------------|--------------------|-----------------------------------------------------------------------------|
| `tweet_id`      | String             | The unique identifier for the tweet, extracted from its URL.                  |
| `username`      | String             | The Twitter/X username of the account that posted the tweet.                  |
| `timestamp`     | Datetime (UTC)     | The Coordinated Universal Time (UTC) when the tweet was published.          |
| `content`       | String             | The full text content of the tweet.                                         |
| `reply_count`   | Integer            | The number of replies to the tweet.                                         |
| `retweet_count` | Integer            | The number of retweets (or reposts).                                        |
| `like_count`    | Integer            | The number of likes on the tweet.                                           |
| `mentions`      | List of Strings    | A list of all usernames mentioned (`@username`) within the tweet content.     |
| `hashtags`      | List of Strings    | A list of all hashtags (`#hashtag`) found within the tweet content.         |