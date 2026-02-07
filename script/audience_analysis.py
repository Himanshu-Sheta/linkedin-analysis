import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

raw_path = os.path.join(DATA_DIR, "audience_raw.csv")
output_path = os.path.join(DATA_DIR, "processed_audience.csv")

if not os.path.exists(raw_path):
    raise FileNotFoundError(f"{raw_path} not found. Export audience_raw.csv first.")

audience_raw = pd.read_csv(raw_path)

# Split headline into role + company (very simple heuristic)
def split_headline(headline: str):
    if not isinstance(headline, str):
        return "", ""
    parts = headline.split(" at ")
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return headline.strip(), ""

audience_raw[["role", "company_type"]] = audience_raw["headline"].apply(
    lambda x: pd.Series(split_headline(x))
)

# Derive seniority from role
def infer_seniority(role: str):
    if not isinstance(role, str):
        return "Mid"
    r = role.lower()
    if "head" in r or "lead" in r or "director" in r or "vp" in r:
        return "Senior"
    if "senior" in r:
        return "Senior"
    if "intern" in r or "junior" in r:
        return "Junior"
    return "Mid"

audience_raw["seniority"] = audience_raw["role"].apply(infer_seniority)

# ICP definition
ICP = {
    "roles": [
        "CTO", "CPO", "Head of Product",
        "Sustainability Lead", "Head of Sustainability"
    ],
    "company_type": ["Fintech", "E-commerce", "Climate Tech"]
}

def score_relevance(row):
    score = 0
    if row["role"] in ICP["roles"]:
        score += 2
    if row["company_type"] in ICP["company_type"]:
        score += 1
    return score

audience_raw["relevance_score"] = audience_raw.apply(score_relevance, axis=1)
audience_processed = audience_raw[["name", "role", "seniority", "company_type", "relevance_score"]]
audience_processed = audience_processed.sort_values("relevance_score", ascending=False)

audience_processed.to_csv(output_path, index=False)
print(f"Audience analysis complete. Saved to {output_path}")
