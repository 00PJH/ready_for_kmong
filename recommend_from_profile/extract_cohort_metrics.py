import json
import pandas as pd
from collections import Counter
import re

with open("c:/workspace/kmong/recommend_from_profile/gigs_details_full.json", "r", encoding="utf-8") as f:
    items = json.load(f)

df = pd.DataFrame(items)

# Define sub-cohorts
df_opt_a = df.sort_values(by=["review_count", "rating_score", "base_price"], ascending=[False, False, False]).head(100)
df_opt_b = df.sort_values(by="ranking_order", ascending=True).head(100)

top_50_b = df.sort_values(by="ranking_order", ascending=True).head(50)
seen = set(top_50_b['gigId'])
hybrid_list = list(top_50_b.to_dict('records'))
for _, r in df_opt_a.iterrows():
    if len(hybrid_list) >= 100:
        break
    if r['gigId'] not in seen:
        seen.add(r['gigId'])
        hybrid_list.append(r.to_dict())
df_opt_c = pd.DataFrame(hybrid_list)

cohorts = {
    "Option_A": df_opt_a,
    "Option_B": df_opt_b,
    "Option_C": df_opt_c
}

def analyze_cohort(name, c_df):
    print(f"\n==================== {name} ====================")
    print(f"Total count: {len(c_df)}")
    print(f"Review Count - Total: {c_df['review_count'].sum()}, Mean: {c_df['review_count'].mean():.1f}, Median: {c_df['review_count'].median()}, Max: {c_df['review_count'].max()}")
    print(f"Rating - Mean: {c_df[c_df['rating_score'] > 0]['rating_score'].mean():.2f}")
    print(f"Base Price - Mean: {c_df['base_price'].mean():,.0f}, Median: {c_df['base_price'].median():,.0f}, Min: {c_df['base_price'].min():,.0f}, Max: {c_df['base_price'].max():,.0f}")
    
    # Seller grades
    print("Seller Grades:", dict(Counter(c_df['seller_grade'])))
    
    # Ads & Prime
    print("Is Ad:", c_df['is_ad'].sum(), "Is Prime:", c_df['is_prime'].sum())
    
    # Keyword extraction from titles
    keywords = []
    for t in c_df['title']:
        words = re.findall(r'[가-힣a-zA-Z0-9]+', t)
        keywords.extend([w for w in words if len(w) > 1 and w not in ['프로그램', '자동화', '제작', '개발', '해드립니다', '구축', '업무', '시스템']])
    top_kw = Counter(keywords).most_common(15)
    print("Top Keywords in Titles:", top_kw)
    
    # Top 5 Sellers by review count or item count
    top_sellers = Counter(c_df['seller_nickname']).most_common(5)
    print("Top Sellers by gig count:", top_sellers)
    
    # AI tools mentioned in metadata
    tools = []
    for t_list in c_df['ai_tools']:
        if isinstance(t_list, list):
            tools.extend(t_list)
    print("Top AI tools:", Counter(tools).most_common(5))
    
    # Sample top 5 gigs
    print("\nTop 5 Gigs Sample:")
    for idx, (_, row) in enumerate(c_df.head(5).iterrows()):
        std_p = row['packages'].get('STANDARD', {}).get('price')
        dlx_p = row['packages'].get('DELUXE', {}).get('price')
        prm_p = row['packages'].get('PREMIUM', {}).get('price')
        print(f"[{idx+1}] ID:{row['gigId']} | {row['title']} | 셀러:{row['seller_nickname']}({row['seller_grade']}) | 리뷰:{row['review_count']}개 | 시작가:{row['base_price']:,}원 | STD:{std_p} DLX:{dlx_p} PRM:{prm_p}")

for name, c_df in cohorts.items():
    analyze_cohort(name, c_df)
