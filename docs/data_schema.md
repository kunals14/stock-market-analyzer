# Data Schema

The project generates data in two main stages: processed and analyzed. The final output is the analyzed data.

### Final Analysis Schema (`trading_signals.parquet`)

This file, located in `data/analysis_results/`, contains the fully processed data with all generated signals and scores.

| Column Name          | Data Type       | Description                                                                 |
|----------------------|-----------------|-----------------------------------------------------------------------------|
| `tweet_id`           | String          | The unique identifier for the tweet.                                        |
| `timestamp`          | Datetime (UTC)  | The UTC timestamp of when the tweet was published.                          |
| `username`           | String          | The username of the account that posted the tweet.                            |
| `content`            | String          | The original, raw text content of the tweet.                                |
| `cleaned_content`    | String          | The normalized text content after cleaning (lowercase, no URLs/mentions).   |
| `reply_count`        | Integer         | The number of replies to the tweet.                                         |
| `retweet_count`      | Integer         | The number of retweets (or reposts).                                        |
| `like_count`         | Integer         | The number of likes on the tweet.                                           |
| `mentions`           | List of Strings | A list of all usernames mentioned (`@username`).                            |
| `hashtags`           | List of Strings | A list of all hashtags (`#hashtag`) found in the content.                   |
| `trading_signal`     | Integer         | The base sentiment polarity score (Positive Words - Negative Words).        |
| `engagement_score`   | Float           | The log-transformed score of all engagement metrics.                        |
| `signal_norm`        | Float (0-1)     | The `trading_signal` normalized to a 0-1 scale.                             |
| `engagement_norm`    | Float (0-1)     | The `engagement_score` normalized to a 0-1 scale.                           |
| `composite_signal`   | Float (0-1)     | The weighted average of the normalized signal and engagement scores.        |
| `confidence`         | Float (0-1)     | The normalized engagement score, used as a proxy for signal confidence.     |