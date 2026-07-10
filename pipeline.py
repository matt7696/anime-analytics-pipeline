import json
from ingest.fetch_anime import fetch_top_anime
from transform.transform_anime import transform_anime, transform_genre, transform_studio
from load.load_anime import (
    connect,
    load_anime_data,
    load_studios_data,
    load_anime_studios_data,
    load_genres_data,
    load_anime_genres_data,
)
import os


def save_raw_data(data, filename="data/raw/raw_anime_data.json"):
    os.makedirs("data/raw", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def save_processed_data(
    anime_df, anime_studios_df, studios_df, anime_genres_df, genres_df
):
    os.makedirs("data/processed", exist_ok=True)
    anime_df.to_csv("data/processed/anime.csv", index=False)
    anime_studios_df.to_csv("data/processed/anime_studios.csv", index=False)
    studios_df.to_csv("data/processed/studios.csv", index=False)
    anime_genres_df.to_csv("data/processed/anime_genres.csv", index=False)
    genres_df.to_csv("data/processed/genres.csv", index=False)


def run_pipeline():
    print("Fetching top anime data...")
    data = fetch_top_anime(6)
    save_raw_data(data)

    print("Transforming data...")
    anime_df = transform_anime(data)
    anime_studios_df, studios_df = transform_studio(data)
    anime_genres_df, genres_df = transform_genre(data)
    save_processed_data(
        anime_df, anime_studios_df, studios_df, anime_genres_df, genres_df
    )

    print("Loading data into the database...")
    conn = connect()
    try:
        load_anime_data(conn, anime_df)
        load_studios_data(conn, studios_df)
        load_genres_data(conn, genres_df)
        load_anime_studios_data(conn, anime_studios_df)
        load_anime_genres_data(conn, anime_genres_df)
    finally:
        conn.close()

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
