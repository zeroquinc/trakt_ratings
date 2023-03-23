# Trakt Ratings for Discord
Embedded Discord Trakt Ratings with clickable links to Trakt and IMDB.
It fetches the API every minute and checks for new ratings.

# Configuration

Make sure you fill in the following values in the `config.json` file:

| Command | Description |
| --- | --- |
| `webhook_url` | The Discord webhook url |
| `trakt_username` | Your Trakt username |
| `client_id` | Your Trakt Client ID |
| `api_key` | Your TMDB API key |
| `timezone` | Your timezone |
| `episode_spoiler` | Spoiler tag for episode overview |
| `season_spoiler` | Spoiler tag for season overview |
| `movie_spoiler` | Spoiler tag for movie overview |

# Examples

Episode Ratings

![image](https://user-images.githubusercontent.com/39315068/227069035-ba5b1324-3a90-41e6-a14e-b432ff75e7d3.png)

Season Ratings

![image](https://user-images.githubusercontent.com/39315068/227069005-5aa657f8-ffdb-4cc3-bc95-ca1dcf34c1a1.png)

Movie Ratings

![image](https://user-images.githubusercontent.com/39315068/227069058-76325a8b-f955-41d2-9ba5-63d4344c17f5.png)

# How to Run

You can install the required packages with the command: `pip3 install -r requirements.txt`

You can for example create a service file and let it run in the background.

```[Unit]
Description=Trakt Ratings
After=network.target

[Service]
Type=simple
User=username
ExecStart=/usr/bin/python3 /opt/scripts/trakt_ratings.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
