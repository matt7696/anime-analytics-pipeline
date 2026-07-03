import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

load_dotenv()

def connect():
    return psycopg2.connect(
        host="localhost",
        database="anipipe",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )
    

def load_anime_data(conn, anime_df):
    values = anime_df.astype(object).where(pd.notnull(anime_df), None).values.tolist()
    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO anime (mal_id, title, type, source, episodes, status, aired_from, aired_to, duration, score, scored_by, rank, popularity, members, favorites, season, year)
            VALUES %s
            ON CONFLICT (mal_id) DO UPDATE SET
                status = EXCLUDED.status,
                aired_from = EXCLUDED.aired_from,
                aired_to = EXCLUDED.aired_to,
                score = EXCLUDED.score,
                scored_by = EXCLUDED.scored_by,
                rank = EXCLUDED.rank,
                popularity = EXCLUDED.popularity,
                members = EXCLUDED.members,
                favorites = EXCLUDED.favorites
        """, values)
        conn.commit()
        
def load_anime_studios_data(conn, anime_studios_df):
    values = anime_studios_df.values.tolist()
    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO anime_studios (anime_id, studio_id)
            VALUES %s
            ON CONFLICT (anime_id, studio_id) DO NOTHING
        """, values)
        conn.commit()

def load_studios_data(conn, studios_df):
    values = studios_df.values.tolist()
    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO studios (mal_id, name)
            VALUES %s
            ON CONFLICT (mal_id) DO NOTHING
        """, values)
        conn.commit()

def load_anime_genres_data(conn, anime_genres_df):
    values = anime_genres_df.values.tolist()
    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO anime_genres (anime_id, genre_id)
            VALUES %s
            ON CONFLICT (anime_id, genre_id) DO NOTHING
        """, values)
        conn.commit()

def load_genres_data(conn, genres_df):
    values = genres_df.values.tolist()
    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO genres (mal_id, name)
            VALUES %s
            ON CONFLICT (mal_id) DO NOTHING
        """, values)
        conn.commit()

if __name__ == "__main__":
    conn = connect()
    
    anime_df = pd.read_csv("data/processed/anime.csv")
    anime_studios_df = pd.read_csv("data/processed/anime_studios.csv")
    studios_df = pd.read_csv("data/processed/studios.csv")
    anime_genres_df = pd.read_csv("data/processed/anime_genres.csv")
    genres_df = pd.read_csv("data/processed/genres.csv")

    load_anime_data(conn, anime_df)
    load_studios_data(conn, studios_df)
    load_anime_studios_data(conn, anime_studios_df)
    load_genres_data(conn, genres_df)
    load_anime_genres_data(conn, anime_genres_df)

    conn.close()