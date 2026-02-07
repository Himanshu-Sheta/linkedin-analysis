import streamlit as st
import pandas as pd
import os

st.title("LinkedIn Analytics Dashboard")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

posts_path = os.path.join(DATA_DIR, "processed_posts.csv")
comments_path = os.path.join(DATA_DIR, "processed_comments.csv")
audience_path = os.path.join(DATA_DIR, "processed_audience.csv")

# Load posts
if os.path.exists(posts_path):
    posts_df = pd.read_csv(posts_path)
else:
    st.error("processed_posts.csv not found. Run scripts/post_analysis.py first.")
    st.stop()

# Load comments (optional)
if os.path.exists(comments_path):
    comments_df = pd.read_csv(comments_path)
else:
    comments_df = None
    st.warning("processed_comments.csv not found. Comment section will be empty.")

# Load audience
if os.path.exists(audience_path):
    audience_df = pd.read_csv(audience_path)
else:
    st.error("processed_audience.csv not found. Run scripts/audience_analysis.py first.")
    st.stop()

st.header("Post Performance")
st.dataframe(posts_df)

st.header("Audience Relevance")
st.dataframe(audience_df)

st.header("Top Post by Predicted Engagement")
if "predicted_engagement" in posts_df.columns:
    st.write(posts_df.sort_values("predicted_engagement", ascending=False).head(1))
else:
    st.write("No predicted_engagement column found in processed_posts.csv")

if comments_df is not None:
    st.header("Comments Overview")
    st.dataframe(comments_df.head())
