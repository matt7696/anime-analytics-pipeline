from fetch_anime import fetch_top_anime
from transform_anime import transform_anime, transform_genre, transform_studio
from load_anime import (
    connect,
    load_anime_data,
    load_studios_data,
    load_anime_studios_data,
    load_genres_data,
    load_anime_genres_data,
)


def run_pipeline():
    print("Fetching top anime data...")
    data = fetch_top_anime(6)

    print("Transforming data...")
    anime_df = transform_anime(data)
    anime_studios_df, studios_df = transform_studio(data)
    anime_genres_df, genres_df = transform_genre(data)

    print("Loading data into the database...")
    conn = connect()
    load_anime_data(conn, anime_df)
    load_studios_data(conn, studios_df)
    load_genres_data(conn, genres_df)
    load_anime_studios_data(conn, anime_studios_df)
    load_anime_genres_data(conn, anime_genres_df)
    conn.close()

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
