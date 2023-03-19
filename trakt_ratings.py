import requests
import json
import time
from datetime import datetime, timedelta
import pytz
from dateutil import parser

# Discord Webhook URL
webhook_url = ""

# Trakt Username
trakt_username = ""

# How many times it needs to check for ratings in minutes
ratings_time = 30

# Trakt API endpoint URLs
episode_ratings_url = f"https://api.trakt.tv/users/{trakt_username}/ratings/episodes"
movie_ratings_url = f"https://api.trakt.tv/users/{trakt_username}/ratings/movies"
season_ratings_url = f"https://api.trakt.tv/users/{trakt_username}/ratings/seasons"

# Trakt client ID
client_id = ""

# TMDB API endpoint URLs
search_url = "https://api.themoviedb.org/3/search/multi"

# TMDB API key
api_key = ""

# Timezone
timezone = pytz.timezone('Europe/Amsterdam')

def send_discord_notification(title, description, trakt_url, show_title, tmdb_id, media_type):
    # Search for show or movie by title
    search_params = {
        "api_key": api_key,
        "query": show_title
    }
    search_response = requests.get(search_url, params=search_params)

    # Parse JSON response for search results
    search_data = json.loads(search_response.text)

    # Check if search results exist
    if len(search_data["results"]) > 0:
        if search_data["results"][0]["media_type"] == "tv" and search_data["results"][0]["poster_path"] is not None:
            poster_url = "https://image.tmdb.org/t/p/w500" + search_data["results"][0]["poster_path"]
        elif search_data["results"][0]["media_type"] == "movie" and search_data["results"][0]["poster_path"] is not None:
            poster_url = "https://image.tmdb.org/t/p/w500" + search_data["results"][0]["poster_path"]
        else:
            poster_url = None
    else:
        poster_url = None

    # Create embedded notification
    if media_type == "episode":
        author_name = "Trakt: Episode Rated"
    elif media_type == "season":
        author_name = "Trakt: Season Rated"
    else:
        author_name = "Trakt: Item Rated"

    embed = {
        "title": title,
        "color": 13506070,
        "timestamp": datetime.utcnow().isoformat(),
        "author": {
            "name": author_name,
            "icon_url": "https://i.imgur.com/Oi3G5Ck.png"
        },
        "fields": [
            {
                "name": "Rating",
                "value": f"{description} :star:",
                "inline": True
            },
            {
                "name": "User",
                "value": f"[{trakt_username}](https://trakt.tv/users/{trakt_username})",
                "inline": True
            },
            {
                "name": "Details",
                "value": f"[Trakt]({trakt_url})",
                "inline": True
            }
        ]
    }

    # Add poster to embedded notification
    if poster_url:
        embed["thumbnail"] = {"url": poster_url}
    # Create Discord notification payload
    payload = {
        "embeds": [embed]
    }

    # Send notification to Discord webhook
    requests.post(webhook_url, json=payload)

def get_recent_ratings():
    # Get current time in Amsterdam timezone
    current_time = datetime.now(timezone)

    # Calculate start time and end time for ratings search
    end_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    start_time = (current_time - timedelta(minutes=(ratings_time))).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # Add headers for Trakt API authorization
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": client_id
    }
    
    #Fetch recent season ratings
    season_params = {
        "start_at": start_time,
        "end_at": end_time
    }
    season_response = requests.get(season_ratings_url, headers=headers, params=season_params)

    # Fetch recent episode ratings
    episode_params = {
        "start_at": start_time,
        "end_at": end_time
    }
    episode_response = requests.get(episode_ratings_url, headers=headers, params=episode_params)

    # Fetch recent movie ratings
    movie_params = {
        "start_at": start_time,
        "end_at": end_time
    }
    movie_response = requests.get(movie_ratings_url, headers=headers, params=movie_params)

    # Parse JSON response for episode ratings
    episode_data = json.loads(episode_response.text)
    for episode in episode_data:
        rating_time = parser.parse(episode["rated_at"]).astimezone(timezone)
        if current_time - rating_time <= timedelta(minutes=(ratings_time)):
            show_title = episode["show"]["title"]
            show_year = episode["show"]["year"]
            season = episode["episode"]["season"]
            episode_number = episode["episode"]["number"]
            episode_title = episode["episode"]["title"]
            episode_slug = episode["show"]["ids"]["slug"]
            episode_id = f"S{season:02d}E{episode_number:02d}"
            title = f"{show_title} - {episode_title} ({episode_id})"
            description = f"{episode['rating']}"
            trakt_url = f"https://trakt.tv/shows/{episode_slug}/seasons/{season}/episodes/{episode_number}"
            tmdb_id = episode["show"]["ids"]["tmdb"]
            send_discord_notification(title, description, trakt_url, show_title, tmdb_id, media_type="episode")
            
    # Parse JSON response for season ratings
    season_data = json.loads(season_response.text)
    for season in season_data:
        rating_time = parser.parse(season["rated_at"]).astimezone(timezone)
        if current_time - rating_time <= timedelta(minutes=(ratings_time)):
            show_title = season["show"]["title"]
            show_year = season["show"]["year"]
            season_number = season["season"]["number"]
            title = f"{show_title} - Season {season_number}"
            description = season["rating"]
            trakt_url = f"https://trakt.tv/shows/{season['show']['ids']['slug']}/seasons/{season_number}"
            tmdb_id = None # Not applicable for seasons
            send_discord_notification(title, description, trakt_url, show_title, tmdb_id, media_type="season")

    # Parse JSON response for movie ratings
    movie_data = json.loads(movie_response.text)
    for movie in movie_data:
        rating_time = parser.parse(movie["rated_at"]).astimezone(timezone)
        if current_time - rating_time <= timedelta(minutes=(ratings_time)):
            title = movie["title"]
            description = f"{movie['rating']}"
            send_discord_notification(title, description)

# Fetch recent ratings and send notifications
while True:
    get_recent_ratings()
    exit()
