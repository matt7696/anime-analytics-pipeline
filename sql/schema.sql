CREATE TABLE anime (
    mal_id INT PRIMARY KEY,
    title TEXT,
    type TEXT,
    source TEXT,
    episodes INT,
    status TEXT,
    aired_from DATE,
    aired_to DATE,
    duration TEXT,
    score REAL,
    scored_by BIGINT,
    rank INT,
    popularity INT,
    members BIGINT,
    favorites BIGINT,
    season TEXT,
    year INT
);

CREATE TABLE genres (
    mal_id INT PRIMARY KEY,
    name TEXT
);

CREATE TABLE anime_genres (
    anime_id INT REFERENCES anime(mal_id),
    genre_id INT REFERENCES genres(mal_id),
    PRIMARY KEY (anime_id, genre_id)
);

CREATE TABLE studios (
    mal_id INT PRIMARY KEY,
    name TEXT
);

CREATE TABLE anime_studios (
    anime_id INT REFERENCES anime(mal_id),
    studio_id INT REFERENCES studios(mal_id),
    PRIMARY KEY (anime_id, studio_id)
);