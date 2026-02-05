import pandas as pd
import psycopg2
from db import get_connection, create_tables

# -----------------------------
# 1. Load your CSVs
# -----------------------------
posts_df = pd.read_csv("post_features.csv")
audience_df = pd.read_csv("audience_analysis.csv")

print("Posts CSV Columns:", posts_df.columns.tolist())
print("Audience CSV Columns:", audience_df.columns.tolist())

# -----------------------------
# 2. Connect to PostgreSQL
# -----------------------------
conn = get_connection()
cursor = conn.cursor()

# Create tables if missing
create_tables(cursor)
conn.commit()

# -----------------------------
# 3. Insert posts
# -----------------------------
for _, row in posts_df.iterrows():
    cursor.execute("""
        INSERT INTO posts (text, hashtags, sentiment, word_count, char_count, predicted_engagement)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        "No text provided",          # because your CSV has no text column
        row["hashtags_count"],       # storing hashtag count instead of text
        row["sentiment"],
        row["word_count"],
        row["char_count"],
        row["predicted_engagement"]
    ))

    post_id = cursor.fetchone()[0]

    # Insert audience rows for each post
    for _, a_row in audience_df.iterrows():
        cursor.execute("""
            INSERT INTO audience (post_id, name, role, seniority, company_type, relevance_score)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            post_id,
            a_row["name"],
            a_row["role"],
            a_row["seniority"],
            a_row["company_type"],
            a_row["relevance_score"]
        ))

conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully.")
