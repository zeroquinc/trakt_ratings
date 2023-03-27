import os
import requests
import json
import time
from datetime import datetime, timedelta
import pytz
from dateutil import parser

# Load configuration from config.json file
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Discord Webhook URL
webhook_url = config['webhook_url']

# Trakt Username
trakt_username = config['trakt_username']

# Trakt client ID
client_id = config['client_id']

# TMDB API key
api_key = config['api_key']

# Timezone
timezone = pytz.timezone(config['timezone'])

# Spoiler
episode_spoiler = config['episode_spoiler']
season_spoiler = config['season_spoiler']
movie_spoiler = config['movie_spoiler']
show_spoiler = config['show_spoiler']

# TMDB API endpoint URLs
search_url = "https://api.themoviedb.org/3/search/multi"

# Trakt API endpoint URLs
episode_ratings_url = f"https://api.trakt.tv/users/{trakt_username}/ratings/episodes"
movie_ratings_url = f"https://api.trakt.tv/users/{trakt_username}/ratings/movies"
season_ratings_url = f"https://api.trakt.tv/users/{trakt_username}/ratings/seasons"
show_ratings_url = f"https://api.trakt.tv/users/{trakt_username}/ratings/shows"

def send_show_notification(title, description, trakt_url, show_title, tmdb_id, show_slug, imdb_id, trakt_id):
    
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
        if search_data["results"][0]["poster_path"] is not None:
            poster_url = "https://image.tmdb.org/t/p/w500" + search_data["results"][0]["poster_path"]
        else:
            poster_url = None
    else:
        poster_url = None

    # Add headers for Trakt API authorization
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": client_id
    }
    
    # Fetch show overview
    show_params = {
        "extended": "full"
    }
    show_response = requests.get(f"https://api.trakt.tv/shows/{trakt_id}", headers=headers, params=show_params)
    show_data = json.loads(show_response.text)
    
    # Get the overview for the show data
    if show_data.get('overview'):
        overview = show_data['overview']
        spoiler = "||" if show_spoiler else ""  # Set spoiler based on show_spoiler value
    else:
        overview = "No overview available"
        spoiler = ""
        
    # Create embedded notification
    author_name = "Trakt: Show Rated"

    embed = {
        "title": title,
        "color": 13506070,
        "timestamp": datetime.utcnow().isoformat(),
        "author": {
            "name": author_name,
            "icon_url": "https://i.imgur.com/poGtHrf.png"
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
                "value": f"[Trakt]({trakt_url}) / [IMDb](https://imdb.com/title/{imdb_id})",
                "inline": True
            },
            {
                "name": "Overview",
                "value": f"{spoiler}{overview}{spoiler}",
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
    requests.post(webhook_url, json=payload).headers

def send_episode_notification(title, description, episode_slug, season, episode_number, trakt_url, show_title, tmdb_id, imdb_id):
    
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
        if search_data["results"][0]["poster_path"] is not None:
            poster_url = "https://image.tmdb.org/t/p/w500" + search_data["results"][0]["poster_path"]
        else:
            poster_url = None
    else:
        poster_url = None

    # Add headers for Trakt API authorization
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": client_id
    }
    
    # Fetch episode overview
    episode_params = {
        "extended": "full"
    }
    episode_response = requests.get(f"https://api.trakt.tv/shows/{episode_slug}/seasons/{season}/episodes/{episode_number}", headers=headers, params=episode_params)
    episode_data = json.loads(episode_response.text)
    
    # Get the overview for the episode data
    if episode_data.get('overview'):
        overview = episode_data['overview']
        spoiler = "||" if episode_spoiler else ""  # Set spoiler based on episode_spoiler value
    else:
        overview = "No overview available"
        spoiler = ""
        
    # Create embedded notification
    author_name = "Trakt: Episode Rated"

    embed = {
        "title": title,
        "color": 13506070,
        "timestamp": datetime.utcnow().isoformat(),
        "author": {
            "name": author_name,
            "icon_url": "https://i.imgur.com/poGtHrf.png"
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
                "value": f"[Trakt]({trakt_url}) / [IMDb](https://imdb.com/title/{imdb_id})",
                "inline": True
            },
            {
                "name": "Overview",
                "value": f"{spoiler}{overview}{spoiler}",
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

def send_season_notification(title, description, trakt_url, show_title, tmdb_id, season_number, season_slug, imdb_id):
    
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
        if search_data["results"][0]["poster_path"] is not None:
            poster_url = "https://image.tmdb.org/t/p/w500" + search_data["results"][0]["poster_path"]
        else:
            poster_url = None
    else:
        poster_url = None

    # Add headers for Trakt API authorization
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": client_id
    }
    
    # Fetch season overview
    season_params = {
        "extended": "full"
    }
    season_response = requests.get(f"https://api.trakt.tv/shows/{season_slug}/seasons", headers=headers, params=season_params)
    season_data = json.loads(season_response.text)

    # Filter the season data based on the season number
    filtered_season_data = [s for s in season_data if s['number'] == season_number]
        
    # Get the overview for the filtered season data
    if filtered_season_data and filtered_season_data[0].get('overview'):
        overview = filtered_season_data[0]['overview']
        spoiler = "||" if season_spoiler else ""  # Set spoiler based on discord_spoiler value
    else:
        overview = "No overview available"
        spoiler = ""

    # Create embedded notification
    author_name = "Trakt: Season Rated"

    embed = {
        "title": title,
        "color": 13506070,
        "timestamp": datetime.utcnow().isoformat(),
        "author": {
            "name": author_name,
            "icon_url": "https://i.imgur.com/poGtHrf.png"
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
                "value": f"[Trakt]({trakt_url})  / [IMDb](https://imdb.com/title/{imdb_id}/episodes?season={season_number})",
                "inline": True
            },
            {
                "name": "Overview",
                "value": f"{spoiler}{overview}{spoiler}",
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

def send_movie_notification(title, description, movie_title, movie_year, trakt_url, tmdb_id, movie_slug, imdb_id):
    
    # Search for show or movie by title
    search_params = {
        "api_key": api_key,
        "query": movie_title
    }
    search_response = requests.get(search_url, params=search_params)

    # Parse JSON response for search results
    search_data = json.loads(search_response.text)

    # Check if search results exist
    if len(search_data["results"]) > 0:
        if search_data["results"][0]["poster_path"] is not None:
            poster_url = "https://image.tmdb.org/t/p/w500" + search_data["results"][0]["poster_path"]
        else:
            poster_url = None
    else:
        poster_url = None

    # Add headers for Trakt API authorization
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": client_id
    }
    
    # Fetch movie overview
    movie_params = {
        "extended": "full"
    }
    movie_response = requests.get(f"https://api.trakt.tv/movies/{movie_slug}", headers=headers, params=movie_params)
    movie_data = json.loads(movie_response.text)
    
    # Get the overview for the movie data
    if movie_data.get('overview'):
        overview = movie_data['overview']
        spoiler = "||" if movie_spoiler else ""  # Set spoiler based on discord_spoiler value
    else:
        overview = "No overview available"
        spoiler = ""

    # Create embedded notification
    author_name = "Trakt: Movie Rated"

    embed = {
        "title": title,
        "color": 13506070,
        "timestamp": datetime.utcnow().isoformat(),
        "author": {
            "name": author_name,
            "icon_url": "https://i.imgur.com/fjWQwef.png"
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
                "value": f"[Trakt]({trakt_url}) / [IMDb](https://imdb.com/title/{imdb_id})",
                "inline": True
            },
            {
                "name": "Overview",
                "value": f"{spoiler}{overview}{spoiler}",
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
    start_time = (current_time - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

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

     #Fetch recent show ratings
    show_params = {
        "start_at": start_time,
        "end_at": end_time
    }
    show_response = requests.get(show_ratings_url, headers=headers, params=show_params)
    
    # Parse JSON response for show ratings
    show_data = json.loads(show_response.text)
    for show in show_data:
        rating_time = parser.parse(show["rated_at"]).astimezone(timezone)
        if current_time - rating_time <= timedelta(minutes=1):
            show_title = show["show"]["title"]
            show_slug = show["show"]["ids"]["slug"]
            trakt_id = show["show"]["ids"]["trakt"]
            imdb_id = show["show"]["ids"]["imdb"]
            show_year = show["show"]["year"]
            title = f"{show_title} ({show_year})"
            description = show["rating"]
            trakt_url = f"https://trakt.tv/shows/{show_slug}"
            tmdb_id = show["show"]["ids"]["tmdb"]
            send_show_notification(title, description, trakt_url, show_title, tmdb_id, show_slug, imdb_id, trakt_id)

    # Parse JSON response for episode ratings
    episode_data = json.loads(episode_response.text)
    for episode in episode_data:
        rating_time = parser.parse(episode["rated_at"]).astimezone(timezone)
        if current_time - rating_time <= timedelta(minutes=1):
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
            imdb_id = episode["episode"]["ids"]["imdb"]
            send_episode_notification(title, description, episode_slug, season, episode_number, trakt_url, show_title, tmdb_id, imdb_id)
            
    # Parse JSON response for season ratings
    season_data = json.loads(season_response.text)
    for season in season_data:
        rating_time = parser.parse(season["rated_at"]).astimezone(timezone)
        if current_time - rating_time <= timedelta(minutes=1):
            show_title = season["show"]["title"]
            season_slug = season["show"]["ids"]["slug"]
            show_year = season["show"]["year"]
            season_number = season["season"]["number"]
            title = f"{show_title} - Season {season_number}"
            description = season["rating"]
            trakt_url = f"https://trakt.tv/shows/{season_slug}/seasons/{season_number}"
            imdb_id = season["show"]["ids"]["imdb"]
            tmdb_id = None # Not applicable for seasons
            send_season_notification(title, description, trakt_url, show_title, tmdb_id, season_number, season_slug, imdb_id)

    # Parse JSON response for movie ratings
    movie_data = json.loads(movie_response.text)
    for movie in movie_data:
        rating_time = parser.parse(movie["rated_at"]).astimezone(timezone)
        if current_time - rating_time <= timedelta(minutes=1):
            movie_title = movie["movie"]["title"]
            description = f"{movie['rating']}"
            movie_year = movie["movie"]["year"]
            title = f"{movie_title} ({movie_year})"
            movie_slug = movie["movie"]["ids"]["slug"]
            trakt_url = f"https://trakt.tv/movies/{movie_slug}"
            tmdb_id = movie["movie"]["ids"]["tmdb"]
            imdb_id = movie["movie"]["ids"]["imdb"]
            send_movie_notification(title, description, movie_title, movie_year, trakt_url, tmdb_id, movie_slug, imdb_id)

# Fetch recent ratings and send notifications
while True:
    get_recent_ratings()
    time.sleep(60)