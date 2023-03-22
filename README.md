# Trakt Ratings for Discord
Embedded Discord Trakt Ratings with clickable links and the plot / overview in a spoiler tag.

# Examples

Episode Ratings:

![image](https://user-images.githubusercontent.com/39315068/227022797-2844f122-e7e8-4af2-9116-c331ddfea860.png)

Season Ratings:

![image](https://user-images.githubusercontent.com/39315068/227022956-f7de16fa-c8a7-4a5d-9308-ae32a87d1e61.png)

Movie Ratings:

![image](https://user-images.githubusercontent.com/39315068/227023093-3601b075-67ea-4a73-b7dc-9c7beb2e439c.png)

# Explanation

Make sure you fill in the following values:

`webhook_url` = Your Discord Webhook URL

`trakt_username` = Your Trakt Username

`client_id` = Trakt client ID

`api_key` = TMDB API Key for posters in the thumbnail

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
