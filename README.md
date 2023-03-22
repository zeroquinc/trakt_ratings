# Trakt Ratings for Discord
Embedded Discord Trakt Ratings with clickable links to Trakt.
It fetches the API every minute and checks for new ratings.

# Explanation

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

Episode Ratings:

![image](https://user-images.githubusercontent.com/39315068/227022797-2844f122-e7e8-4af2-9116-c331ddfea860.png)

Season Ratings:

![image](https://user-images.githubusercontent.com/39315068/227022956-f7de16fa-c8a7-4a5d-9308-ae32a87d1e61.png)

Movie Ratings:

![image](https://user-images.githubusercontent.com/39315068/227023093-3601b075-67ea-4a73-b7dc-9c7beb2e439c.png)

# How to Run

Make sure you have python3 installed with pip3 and the `requests` module.

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
