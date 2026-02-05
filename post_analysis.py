import pandas as pd
from db import get_connection, create_tables

# Helper to convert NumPy types → pure Python
def to_python(value):
    try:
        return value.item()  # converts numpy types
    except AttributeError:
        return value

# -----------------------------
# 1. Load your CSVs
# -----------------------------
posts_df = pd.read_csv("linkedin_posts.csv")
audience_df = pd.read_csv("audience_analysis.csv")

print("Posts CSV Columns:", posts_df.columns.tolist())
print("Audience CSV Columns:", audience_df.columns.tolist())

# -----------------------------
# 2. Connect to PostgreSQL
# -----------------------------
conn = get_connection()
cursor = conn.cursor()

# TEMPORARY: Drop old tables to remove wrong schema
cursor.execute("DROP TABLE IF EXISTS audience CASCADE;")
cursor.execute("DROP TABLE IF EXISTS posts CASCADE;")

# Recreate tables with correct schema
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
        to_python(row["hashtags_count"]),
        to_python(row["sentiment"]),
        to_python(row["word_count"]),
        to_python(row["char_count"]),
        to_python(row["predicted_engagement"])
    ))

    post_id = cursor.fetchone()[0]

    # Insert audience rows for each post
    for _, a_row in audience_df.iterrows():
        cursor.execute("""
            INSERT INTO audience (post_id, name, role, seniority, company_type, relevance_score)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            post_id,
            to_python(a_row["name"]),
            to_python(a_row["role"]),
            to_python(a_row["seniority"]),
            to_python(a_row["company_type"]),
            to_python(a_row["relevance_score"])
        ))

conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully.")
