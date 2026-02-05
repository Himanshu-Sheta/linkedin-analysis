import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from db import get_connection, create_tables

# -----------------------------
# 1. Load your CSV or data
# -----------------------------
df = pd.read_csv("linkedin_posts.csv")  # adjust if needed

# -----------------------------
# 2. Feature Engineering
# -----------------------------
def extract_hashtags(text):
    return " ".join([word for word in text.split() if word.startswith("#")])

df["hashtags"] = df["text"].apply(extract_hashtags)
df["sentiment"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)
df["word_count"] = df["text"].apply(lambda x: len(x.split()))
df["char_count"] = df["text"].apply(len)

# -----------------------------
# 3. Simple Engagement Model
# -----------------------------
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["text"])
y = df["engagement"] if "engagement" in df.columns else np.random.rand(len(df))

model = LinearRegression()
model.fit(X, y)

df["predicted_engagement"] = model.predict(X)

# -----------------------------
# 4. Save CSV (optional)
# -----------------------------
df.to_csv("processed_posts.csv", index=False)
print("Post analysis complete. CSV saved.")

# -----------------------------
# 5. Insert into PostgreSQL
# -----------------------------
conn = get_connection()
cursor = conn.cursor()

# Create tables if missing
create_tables(cursor)
conn.commit()

# Insert posts
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO posts (text, hashtags, sentiment, word_count, char_count, predicted_engagement)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        row["text"],
        row["hashtags"],
        row["sentiment"],
        row["word_count"],
        row["char_count"],
        row["predicted_engagement"]
    ))

    post_id = cursor.fetchone()[0]

    # Insert dummy audience data (replace with real logic)
    cursor.execute("""
        INSERT INTO audience (post_id, name, role, seniority, company_type, relevance_score)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        post_id,
        "John Doe",
        "Engineer",
        "Mid",
        "Tech",
        85
    ))

conn.commit()
cursor.close()
conn.close()

print("Data inserted into PostgreSQL successfully.")
