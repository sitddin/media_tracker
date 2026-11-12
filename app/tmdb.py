import os

import httpx
from dotenv import load_dotenv

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_TOKEN")

TMDB_URL = "https://api.themoviedb.org/3/search/movie"

def search_movies(title: str):
    if not TMDB_TOKEN:
        raise RuntimeError("TMDB_TOKEN is not configured")

    headers = {
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }

    params = {
        "query": title,
        "language": "ru-RU"
    }

    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            TMDB_URL,
            headers=headers,
            params=params
        )

        response.raise_for_status()

        return response.json()

def get_movie_details(tmdb_id: int):
    if not TMDB_TOKEN:
        raise RuntimeError("TMDB_TOKEN is not configured")

    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"

    headers= {
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }

    params = {
        "language": "ru-RU"
    }
    \
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            url,
            headers=headers,
            params=params
        )

        response.raise_for_status()
        return response.json()