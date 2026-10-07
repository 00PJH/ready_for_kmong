import json
import pandas as pd
import numpy as np

DATA_PATH = "c:/workspace/kmong/recommend_from_profile/gigs_details_full.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total loaded items: {len(items)}")

df = pd.DataFrame(items)
print("Columns:", df.columns.tolist())

# Check reviews and ratings
df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce').fillna(0).astype(int)
df['rating_score'] = pd.to_numeric(df['rating_score'], errors='coerce').fillna(0.0).astype(float)
df['base_price'] = pd.to_numeric(df['base_price'], errors='coerce').fillna(0).astype(int)

# Score for Option A: review_count * rating_score (or review_count primary, rating secondary)
df['weighted_score'] = df['review_count'] * df['rating_score']

print("Top 10 by review count:")
top_reviews = df.sort_values(by=['review_count', 'rating_score', 'base_price'], ascending=[False, False, False]).head(10)
for _, r in top_reviews[['gigId', 'title', 'seller_nickname', 'seller_grade', 'review_count', 'rating_score', 'base_price']].iterrows():
    print(r.to_dict())

print("\nTop 10 by ranking order (Option B):")
top_ranking = df.sort_values(by='ranking_order', ascending=True).head(10)
for _, r in top_ranking[['ranking_order', 'gigId', 'title', 'seller_nickname', 'seller_grade', 'review_count', 'rating_score', 'base_price']].iterrows():
    print(r.to_dict())

# Summary stats
print("\nStats:")
print("Review count sum:", df['review_count'].sum())
print("Items with > 0 reviews:", (df['review_count'] > 0).sum())
print("Items with >= 10 reviews:", (df['review_count'] >= 10).sum())
print("Items with >= 50 reviews:", (df['review_count'] >= 50).sum())
print("Items with >= 100 reviews:", (df['review_count'] >= 100).sum())
print("Base price median:", df['base_price'].median(), "mean:", df['base_price'].mean())
print("Max reviews:", df['review_count'].max())
