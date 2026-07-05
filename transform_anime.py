import json
import pandas as pd


def load_raw(filepath: str) -> list[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def transform_anime(raw_data: list[dict]) -> pd.DataFrame:
    transformed = []
    for anime in raw_data:
        transformed.append(
            {
                "mal_id": anime.get("mal_id"),
                "title": anime.get("title"),
                "type": anime.get("type"),
                "source": anime.get("source"),
                "episodes": anime.get("episodes"),
                "status": anime.get("status"),
                "aired_from": (anime.get("aired", {}).get("from") or "")[:10] or None,
                "aired_to": (anime.get("aired", {}).get("to") or "")[:10] or None,
                "duration": anime.get("duration"),
                "score": anime.get("score"),
                "scored_by": anime.get("scored_by"),
                "rank": anime.get("rank"),
                "popularity": anime.get("popularity"),
                "members": anime.get("members"),
                "favorites": anime.get("favorites"),
                "season": anime.get("season"),
                "year": anime.get("year"),
            }
        )

    return pd.DataFrame(transformed)


def transform_studio(raw_data: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    transformed_studios = []
    transformed_anime_studio = []
    studio_ids = set()

    for anime in raw_data:
        for studio in anime.get("studios", []):
            if studio.get("mal_id") not in studio_ids:
                transformed_studios.append(
                    {
                        "mal_id": studio.get("mal_id"),
                        "name": studio.get("name"),
                    }
                )
                studio_ids.add(studio.get("mal_id"))
            transformed_anime_studio.append(
                {
                    "anime_id": anime.get("mal_id"),
                    "studio_id": studio.get("mal_id"),
                }
            )
    return pd.DataFrame(transformed_anime_studio), pd.DataFrame(transformed_studios)


def transform_genre(raw_data: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    transformed_genres = []
    transformed_anime_genre = []
    genre_ids = set()

    for anime in raw_data:
        for genre in anime.get("genres", []):
            if genre.get("mal_id") not in genre_ids:
                transformed_genres.append(
                    {
                        "mal_id": genre.get("mal_id"),
                        "name": genre.get("name"),
                    }
                )
                genre_ids.add(genre.get("mal_id"))
            transformed_anime_genre.append(
                {
                    "anime_id": anime.get("mal_id"),
                    "genre_id": genre.get("mal_id"),
                }
            )
    return pd.DataFrame(transformed_anime_genre), pd.DataFrame(transformed_genres)


if __name__ == "__main__":
    raw_data = load_raw("data/raw/raw_anime_data.json")

    anime = transform_anime(raw_data)
    anime_studios, studios = transform_studio(raw_data)
    anime_genres, genres = transform_genre(raw_data)

    anime.to_csv("data/processed/anime.csv", index=False)
    anime_studios.to_csv("data/processed/anime_studios.csv", index=False)
    studios.to_csv("data/processed/studios.csv", index=False)
    anime_genres.to_csv("data/processed/anime_genres.csv", index=False)
    genres.to_csv("data/processed/genres.csv", index=False)
