## 1. Project Overview

Anipipe is an ETL Data Pipeline that pulls data from MyAnimeList via JikanAPI. Currently it extracts top rated anime and stores that data in a PostgreSQL database. There is also a script that generates bar graphs with Matplotlib displaying some analytics from the data. 

## 2. Tech Stack

Python, PostgreSQL, Pandas, JikanAPI, Psycopg2, Matplotlib


## 3. Pipeline Architecture

Jikan API -> fetch_anime.py -> transform_anime.py -> load_anime.py -> PostgreSQL -> visualize.py

## 4. Schema

The schema is normalized into 5 tables so far to prevent data duplication and allow for join-based analytics.

anime - Anime metrics (mal_id, title, score, season, etc.)

genres - Genre metrics (mal_id, name)

studios - Studio metrics (mal_id, name)

anime_genres - Anime-Genre pairing (foreign key relation with anime & genre id)

anime_studios - Anime-Studio pairing (foreign key relation with anime & studio id)

## 5. How to Run

1. Clone the repo

2. Create a .env file with DB_PASSWORD=yourpassword

3. Create the database: psql -U postgres -c "CREATE DATABASE anipipe;"

4. Run schema: psql -U postgres -d anipipe -f sql/schema.sql

5. pip install -r requirements.txt

6. python pipeline.py

7. python visualize.py

## 6. Visualizations

top_anime_scores.png - Bar graph depicting top 10 highest scored anime

score_by_studio.png - Bar graph depicting top 10 studios with average highest anime score from the data in the database

## 7. Automation

Add line in crontab to update database daily and regenerate charts. Cron runs in WSL with sudo service cron start.

0 9 * * * cd /path/to/anipipe && python3 pipeline.py && python3 visualize.py
