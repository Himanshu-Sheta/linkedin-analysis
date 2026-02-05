import pandas as pd

# -----------------------------------------
# 1. Audience data
# -----------------------------------------
audience = pd.DataFrame({
    "name": [
        "Himanshu Sheta",
        "Iron man",
        "Sam",
        "Tony"
    ],
    "role": [
        "AI & Data Engineer",
        "Head of Sustainability",
        "Climate Policy Lead",
        "Senior Product Marketing Manager"
    ],
    "seniority": [
        "Mid",
        "Senior",
        "Senior",
        "Mid"
    ],
    "company_type": [
        "Tech Startup",
        "Fintech",
        "Climate Tech",
        "Fintech"
    ]
})

# -----------------------------------------
# 2. ICP definition
# -----------------------------------------
ICP = {
    "roles": ["CTO", "CPO", "Head of Product", "Sustainability Lead"],
    "company_type": ["Fintech", "E-commerce"]
}

# -----------------------------------------
# 3. Scoring function
# -----------------------------------------
def score_relevance(row):
    score = 0
    if row["role"] in ICP["roles"]:
        score += 2
    if row["company_type"] in ICP["company_type"]:
        score += 1
    return score

# -----------------------------------------
# 4. Apply scoring
# -----------------------------------------
audience["relevance_score"] = audience.apply(score_relevance, axis=1)
audience = audience.sort_values("relevance_score", ascending=False)

# -----------------------------------------
# 5. Save CSV
# -----------------------------------------
audience.to_csv("audience_analysis.csv", index=False)
print("Audience analysis complete. CSV saved.")
