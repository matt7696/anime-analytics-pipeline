import requests
import time
import json

BASE_URL_ANIME = "https://api.jikan.moe/v4/top/anime"
BASE_URL_MANGA = "https://api.jikan.moe/v4/top/manga"
HEADERS = {"User-Agent": "anime-analytics-pipeline/0.1"}


def fetch_top_anime(pages: int = 1) -> list[dict]:
    all_anime = []
    for page in range(1, pages + 1):
        response = requests.get(BASE_URL_ANIME, headers=HEADERS, params={"page": page})
        response.raise_for_status()
        data = response.json()
        all_anime.extend(data["data"])
        print(f"Page {page}: {len(data['data'])} records fetched")
        time.sleep(1)
    return all_anime

def fetch_top_manga(pages: int = 1) -> list[dict]:
    all_manga = []
    for page in range(1, pages + 1):
        response = requests.get(BASE_URL_MANGA, headers=HEADERS, params={"page": page})
        response.raise_for_status()
        data = response.json()
        all_manga.extend(data["data"])
        print(f"Page {page}: {len(data['data'])} records fetched")
        time.sleep(1)
    return all_manga


if __name__ == "__main__":
    anime = fetch_top_anime(pages=2)
    with open("data/raw/raw_anime_data.json", "w", encoding="utf-8") as f:
        json.dump(anime, f, indent=2, ensure_ascii=False)
    print(f"Done. {len(anime)} records saved to raw_anime_data.json")
    manga = fetch_top_manga(pages=2)
    with open("data/raw/raw_manga_data.json", "w", encoding="utf-8") as f:
        json.dump(manga, f, indent=2, ensure_ascii=False)
    print(f"Done. {len(manga)} records saved to raw_manga_data.json")
