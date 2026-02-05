import pandas as pd
import psycopg2
from db import get_connection, create_tables

# -----------------------------
# 1. Load your CSVs
# -----------------------------
posts_df = pd.read_csv("linkedin_posts.csv")
audience_df = pd.read_csv("audience_analysis.csv")


# Convert all NumPy types to Python native types posts_df = posts_df.astype(object).where(pd.notnull(posts_df), None) audience_df = audience_df.astype(object).where(pd.notnull(audience_df), None)

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
        "No text provided",
        row["hashtags_count"],
        row["sentiment"],
        row["word_count"],
        row["char_count"],
        row["predicted_engagement"]
    ))

    post_id = cursor.fetchone()[0]

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
