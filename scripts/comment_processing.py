import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

comments_path = os.path.join(DATA_DIR, "linkedin_comments.csv")
output_path = os.path.join(DATA_DIR, "processed_comments.csv")

if not os.path.exists(comments_path):
    raise FileNotFoundError(f"{comments_path} not found. Export linkedin_comments.csv first.")

comments_df = pd.read_csv(comments_path)

# Basic cleaning example
if "comment" in comments_df.columns:
    comments_df["comment_clean"] = comments_df["comment"].fillna("").str.strip()
else:
    comments_df["comment_clean"] = ""

# Simple length feature
comments_df["comment_length"] = comments_df["comment_clean"].str.len()

comments_df.to_csv(output_path, index=False)
print(f"Comment processing complete. Saved to {output_path}")
