# Trakt Ratings for Discord
Embedded Discord Trakt Ratings with clickable links.

# Explanation

Make sure you fill in the following values:

`webhook_url` = Your Discord Webhook URL

`trakt_username` = Your Trakt Username

`ratings_time` = The times you want it fetch the Trakt API for ratings in minutes

`client_id` = Trakt client ID

`api_key` = TMDB API Key for posters in the thumbnail

# How to Run

Make sure you have python3 installed with pip3 and the `requests` module.

Make a cron job depending on the `ratings_time`. Make sure the cron job and this value are always the same.

For example: `*/30 * * * * python3 /opt/scripts/trakt_ratings.py`

The above code runs a cronjob every 30 minutes.

# Examples

Episode Ratings:

![image](https://user-images.githubusercontent.com/39315068/226148315-8e217d7d-d2fd-4d23-834a-d2d417fcded8.png)

Season Ratings:

![image](https://user-images.githubusercontent.com/39315068/226148288-b1903331-59a0-4fea-8040-fb286642a369.png)

# To Do

In the future I will also fix the movie part because that is still a bit plain and also gonna try to add a Episode / Season / Movie description in the embed.
