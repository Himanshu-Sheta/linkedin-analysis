import re
import pandas as pd
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
from db import get_connection


# -----------------------------------------
# 1. Paste LinkedIn post text here
# -----------------------------------------
post_text = """
🌍 We’re proud to announce the launch of our AI for Climate Resilience Program.

AI already powers everything we do at Klarna — and now we’re turning that same expertise toward the front lines of climate change. We take pride in our legacy as a climate leader, and we’re committed to driving positive change for the future. The AI for Climate Resilience Program will support pioneering projects that harness artificial intelligence to help climate-vulnerable communities adapt and thrive.

This is technology in service of both people and the planet.

This program will support local, practical, and community-owned solutions. From strengthening food security and improving health systems to building coastal resilience in the face of climate change.

What’s on offer:
💸 Grants of up to $300,000
🧑‍🎓 Mentorship, training, and a supportive community of practice

We encourage applications from organizations working to reduce vulnerability of local communities to climate-related risks in low- and middle-income countries. We welcome early stage applications as well, from teams that need support in developing technical details further. Whether you’re using AI to support smallholder farmers, build early warning systems, or translate complex risk data into community action plans, we want to hear from you!
"""

# Engagement numbers (manually added)
likes = 1200
comments = 150
reposts = 40


# -----------------------------------------
# 2. Extract features
# -----------------------------------------
hashtags = re.findall(r"#\w+", post_text)
sentiment = TextBlob(post_text).sentiment.polarity
word_count = len(post_text.split())
char_count = len(post_text)

# Create dataframe for prediction
features = pd.DataFrame([{
    "word_count": word_count,
    "char_count": char_count,
    "sentiment": sentiment,
    "hashtags_count": len(hashtags),
    "likes": likes,
    "comments": comments,
    "reposts": reposts
}])


# -----------------------------------------
# 3. Mock dataset for prediction
# -----------------------------------------
mock = pd.DataFrame({
    "word_count": [100, 150, 80],
    "sentiment": [0.1, 0.5, -0.2],
    "hashtags_count": [3, 5, 1],
    "engagement": [500, 900, 200]
})

X = mock[["word_count", "sentiment", "hashtags_count"]]
y = mock["engagement"]

model = LinearRegression().fit(X, y)

prediction = model.predict(features[["word_count", "sentiment", "hashtags_count"]])
features["predicted_engagement"] = prediction


# -----------------------------------------
# 4. Save output locally
# -----------------------------------------
features.to_csv("post_features.csv", index=False)
print("Post analysis complete. CSV saved.")


# -----------------------------------------
# 5. Insert into PostgreSQL
# -----------------------------------------
conn = get_connection()
cursor = conn.cursor()

# Insert post into posts table
cursor.execute("""
    INSERT INTO posts (text, hashtags, sentiment, word_count, char_count, predicted_engagement)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
""", (
    post_text,
    ",".join(hashtags),
    sentiment,
    word_count,
    char_count,
    float(prediction[0])
))

post_id = cursor.fetchone()[0]
conn.commit()

print(f"Inserted post into database with ID: {post_id}")


# -----------------------------------------
# 6. Generate mock audience data (example)
# -----------------------------------------
audience = pd.DataFrame([
    {"name": "Alice", "role": "Data Scientist", "seniority": "Mid", "company_type": "Tech", "relevance_score": 85},
    {"name": "Bob", "role": "AI Researcher", "seniority": "Senior", "company_type": "Research Lab", "relevance_score": 92},
    {"name": "Charlie", "role": "Climate Analyst", "seniority": "Junior", "company_type": "NGO", "relevance_score": 78}
])


# -----------------------------------------
# 7. Insert audience rows
# -----------------------------------------
for _, row in audience.iterrows():
    cursor.execute("""
        INSERT INTO audience (post_id, name, role, seniority, company_type, relevance_score)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        post_id,
        row["name"],
        row["role"],
        row["seniority"],
        row["company_type"],
        row["relevance_score"]
    ))

conn.commit()
cursor.close()
conn.close()

print("Audience data inserted successfully.")
