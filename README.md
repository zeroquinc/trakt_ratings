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
| `show_spoiler` | Spoiler tag for show overview |
| `episode_spoiler` | Spoiler tag for episode overview |
| `season_spoiler` | Spoiler tag for season overview |
| `movie_spoiler` | Spoiler tag for movie overview |

# Examples

Movie Ratings

![image](https://user-images.githubusercontent.com/39315068/228053186-0903077a-f612-412d-9c05-ef72608d9ca2.png)

Show Ratings

![image](https://user-images.githubusercontent.com/39315068/228053011-54ba6da5-8e21-41f9-9c84-58f2a8c8a301.png)

Episode Ratings

![image](https://user-images.githubusercontent.com/39315068/228053065-9f1a81ee-ddf9-457f-8132-0703d2104913.png)

Season Ratings

![image](https://user-images.githubusercontent.com/39315068/228053112-13edc762-df58-4b26-b68f-88b103c80da5.png)

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
