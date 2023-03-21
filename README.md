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

![image](https://user-images.githubusercontent.com/39315068/226564147-2b8a7c95-de18-4acc-ab2c-919163e61ef2.png)

Season Ratings:

![image](https://user-images.githubusercontent.com/39315068/226564205-25a8f168-0512-4788-8f25-e50625ccfbf9.png)

Movie Ratings:

![image](https://user-images.githubusercontent.com/39315068/226564346-ebb2c752-a88a-4b9d-9df4-bf2587e8ba0a.png)

# To Do

In the future I will also fix the movie part because that is still a bit plain and also gonna try to add a Episode / Season / Movie description in the embed.
