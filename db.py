import os
import psycopg2


def create_tables(cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY,
        text TEXT,
        hashtags INT,
        sentiment FLOAT,
        word_count INT,
        char_count INT,
        predicted_engagement FLOAT,
        created_at TIMESTAMP DEFAULT NOW()
    );
"""
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audience (
            id SERIAL PRIMARY KEY,
            post_id INT REFERENCES posts(id),
            name VARCHAR(255),
            role VARCHAR(255),
            seniority VARCHAR(255),
            company_type VARCHAR(255),
            relevance_score INT
        );
    """
    )


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "linkedin"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "1234"),
        port=5432,
    )
