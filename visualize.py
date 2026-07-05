import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()


def connect():
    password = os.getenv("DB_PASSWORD")
    return create_engine(f"postgresql+psycopg2://postgres:{password}@localhost/anipipe")


def plot_top_anime(conn):
    df = pd.read_sql(
        """
        SELECT title, score 
        FROM anime 
        ORDER BY score DESC 
        LIMIT 10;
        """,
        conn,
    )

    plt.figure(figsize=(14, 6))
    bars = plt.barh(df["title"], df["score"])

    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 0.05,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.2f}",
            va="center",
        )

    plt.xlabel("Score")
    plt.title("Top 10 Anime by Score")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("charts/top_anime_scores.png")
    plt.close()


def plot_top_studios(conn):
    df = pd.read_sql(
        """
        SELECT s.name, ROUND(AVG(a.score)::numeric, 2) as avg_score, COUNT(ast.anime_id) as anime_count
        FROM studios s
        JOIN anime_studios ast ON s.mal_id = ast.studio_id
        JOIN anime a ON ast.anime_id = a.mal_id
        WHERE a.score IS NOT NULL
        GROUP BY s.name
        ORDER BY avg_score DESC
        LIMIT 10
        """,
        conn,
    )

    plt.figure(figsize=(14, 6))
    bars = plt.barh(df["name"], df["avg_score"])

    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 0.05,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.2f}",
            va="center",
        )

    plt.xlabel("Average Score")
    plt.title("Average Anime Score by Studio")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("charts/score_by_studio.png")
    plt.close()


if __name__ == "__main__":
    os.makedirs("charts", exist_ok=True)
    conn = connect()
    plot_top_anime(conn)
    plot_top_studios(conn)
    conn.dispose()
