import requests
import time
import json

BASE_URL_ANIME = "https://api.jikan.moe/v4/top/anime"
HEADERS = {"User-Agent": "anime-analytics-pipeline/0.1"}


def fetch_top_anime(pages: int = 1) -> list[dict]:
    all_anime = []
    for page in range(1, pages + 1):
        response = requests.get(BASE_URL_ANIME, headers=HEADERS, params={"page": page})
        response.raise_for_status()
        data = response.json()
        all_anime.extend(data["data"])
        time.sleep(1)
    return all_anime


if __name__ == "__main__":
    anime = fetch_top_anime(2)
    with open("data/raw/raw_anime_data.json", "w", encoding="utf-8") as f:
        json.dump(anime, f, indent=2)
