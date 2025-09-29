# Data Schema

The project produces a final, analyzed dataset containing trading signals. This data is stored in the `data/analysis_results/` directory.

### Final Analysis Schema (`trading_signals.parquet`)

This Parquet file contains the fully processed data with all generated signals and scores, ready for analysis or use in a trading algorithm.

| Column Name          | Data Type       | Description                                                                 |
|----------------------|-----------------|-----------------------------------------------------------------------------|
| `tweet_id`           | String          | The unique identifier for the tweet, used for deduplication.                |
| `timestamp`          | Datetime (UTC)  | The UTC timestamp indicating when the tweet was published.                  |
| `username`           | String          | The username of the account that posted the tweet.                          |
| `content`            | String          | The original, raw text content of the tweet.                                |
| `cleaned_content`    | String          | The normalized text content after cleaning (lowercase, no URLs/mentions).   |
| `reply_count`        | Integer         | The number of replies to the tweet.                                         |
| `retweet_count`      | Integer         | The number of retweets (or reposts).                                        |
| `like_count`         | Integer         | The number of likes on the tweet.                                           |
| `mentions`           | List of Strings | A list of all user accounts mentioned (`@username`) in the tweet.           |
| `hashtags`           | List of Strings | A list of all hashtags (`#hashtag`) found in the tweet content.             |
| `trading_signal`     | Integer         | The base sentiment score calculated as (Positive Words - Negative Words).   |
| `engagement_score`   | Float           | A log-transformed score combining replies, retweets, and likes.             |
| `signal_norm`        | Float (0-1)     | The `trading_signal` normalized to a 0-to-1 scale.                          |
| `engagement_norm`    | Float (0-1)     | The `engagement_score` normalized to a 0-to-1 scale.                        |
| `composite_signal`   | Float (0-1)     | The final weighted average of the normalized signal and engagement scores.  |
| `confidence`         | Float (0-1)     | The normalized engagement score, used as a proxy for signal confidence.     |