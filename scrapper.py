import numpy as np
import pandas as pd
import requests
import time
import json
import os


def estimate_max_anime_id():
    url = "https://api.jikan.moe/v4/seasons/now"
    r = requests.get(url)
    data = r.json()["data"]
    return max(anime["mal_id"] for anime in data)


MAX_ANIME_ID = estimate_max_anime_id()


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_to_json(data, filename):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(filename, "r", encoding="utf-8") as f:
        current_data = json.load(f)

    current_data.extend(data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)


def get_json_anime_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        anime_entries = json.load(f)

    results = []
    # print(anime_entries)

    for anime in anime_entries:
        # print(type(anime))
        results.append({
            "mal_id": anime.get("mal_id"),
            "url": anime.get("url"),
            "title_english": anime.get("title_english"),
            "type": anime.get("type"),
            "source": anime.get("source"),
            "episodes": anime.get("episodes"),
            "aired": anime.get("aired", {}).get("string"),
            "duration": anime.get("duration"),
            "rating": anime.get("rating"),
            "score": anime.get("score"),
            "scored_by": anime.get("scored_by"),
            "rank": anime.get("rank"),
            "popularity": anime.get("popularity"),
            "members": anime.get("members"),
            "favorites": anime.get("favorites"),
            "year": anime.get("year"),

            "studios": [
                studio.get("name")
                for studio in anime.get("studios", [])
            ],

            "genres": [
                genre.get("name")
                for genre in anime.get("genres", [])
            ],

            "explicit_genres": [
                genre.get("name")
                for genre in anime.get("explicit_genres", [])
            ],

            "themes": [
                theme.get("name")
                for theme in anime.get("themes", [])
            ]
        })

    return results


def get_json_studios_data(filepath):
    # from test_anime.json
    # 'studios' -> ...

    with open(filepath, "r", encoding="utf-8") as f:
        anime_entries = json.load(f)

    studios = []  # 1 anime can have more than 1 studio, 1->N relation?

    for anime in anime_entries:
        for studio in anime.get("studios", []):
            studios.append({
                "studio_id": studio.get("mal_id"),  # .../producers/{mal_id}
                "studio_name": studio.get("name"),
                "studio_url": studio.get("url"),
                # "anime_id": anime.get('mal_id')  # think about it later
            })

    return studios


def get_safe_data(response):
    try:
        return response.json().get("data")
    except Exception:
        return None


def get_anime(mal_id: int):
    url = f"https://api.jikan.moe/v4/anime/{mal_id}"
    
    while True:
        response = requests.get(url)

        if response.status_code == 200:
            return get_safe_data(response)

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 2))
            print(f'Too many requests. Waiting time: {wait}s. Current anime id: {mal_id}')
            time.sleep(wait)
            continue

        return None


def get_request_anime_entries(min_id, max_id):
    results = []
    valid_ids = []

    for mal_id in range(min_id, max_id + 1):
        anime = get_anime(mal_id)

        if anime is not None:
            results.append(anime)
            valid_ids.append(mal_id)
        
        time.sleep(0.2)

    return results, valid_ids



test_anime_entries, valid_ids = get_request_anime_entries(15001, 30000)
len(test_anime_entries), len(valid_ids)
append_to_json(test_anime_entries, 'data/test_anime.json')

