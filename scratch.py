import json
import requests

BASE_URL_ANIME = "https://api.jikan.moe/v4/top/anime"
HEADERS = {"User-Agent": "anime-analytics-pipeline/0.1"}

response = requests.get(BASE_URL_ANIME, headers=HEADERS, params={"limit": 25})
print(response.status_code)
response.raise_for_status()
data = response.json()

with open("data/raw/test_anime.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)