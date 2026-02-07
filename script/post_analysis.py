import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

posts_path = os.path.join(DATA_DIR, "linkedin_posts.csv")
output_path = os.path.join(DATA_DIR, "processed_posts.csv")

if not os.path.exists(posts_path):
    raise FileNotFoundError(f"{posts_path} not found. Create linkedin_posts.csv first.")

posts_df = pd.read_csv(posts_path)

# Basic safety: ensure required columns
required_cols = ["text", "likes", "comments", "reposts"]
for col in required_cols:
    if col not in posts_df.columns:
        raise ValueError(f"Missing column '{col}' in linkedin_posts.csv")

# Add manual reaction breakdown (example values)
posts_df["like_count"] = 72
posts_df["celebrate_count"] = 13
posts_df["support_count"] = 10
posts_df["love_count"] = 3
posts_df["insightful_count"] = 1
posts_df["total_reactions"] = (
    posts_df["like_count"]
    + posts_df["celebrate_count"]
    + posts_df["support_count"]
    + posts_df["love_count"]
    + posts_df["insightful_count"]
)

# Simple engagement metric
posts_df["engagement_rate"] = (
    posts_df["likes"] + posts_df["comments"] + posts_df["reposts"]
) / posts_df["likes"].replace(0, 1)

# Very simple "predicted engagement" (toy model)
posts_df["predicted_engagement"] = (
    posts_df["likes"] * 0.6
    + posts_df["comments"] * 1.5
    + posts_df["reposts"] * 1.2
)

posts_df.to_csv(output_path, index=False)
print(f"Post analysis complete. Saved to {output_path}")
