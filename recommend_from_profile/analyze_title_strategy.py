import os
import json
import re
from collections import Counter

BASE_DIR = "c:/workspace/kmong"
STRATEGY_DIR = "c:/workspace/kmong/kmong_strategy"

CATS = [
    {"id": 668, "name": "AI 자동화 프로그램", "folder": "AI_자동화_프로그램"},
    {"id": 667, "name": "맞춤형 챗봇·GPT", "folder": "맞춤형_챗봇_GPT"},
    {"id": 670, "name": "이미지·음성 인식", "folder": "이미지_음성_인식"},
    {"id": 651, "name": "AI 시스템·서비스", "folder": "AI_시스템_서비스"}
]

def analyze_category_titles(cat):
    p = os.path.join(BASE_DIR, cat["folder"], "gigs_details_full.json")
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        items = json.load(f)
    items.sort(key=lambda x: (x.get("review_count", 0), x.get("rating_score", 0), x.get("base_price", 0)), reverse=True)
    top10 = items[:10]
    
    titles = [it.get("title", "") for it in top10]
    words = []
    for t in titles:
        found = re.findall(r'[가-힣a-zA-Z0-9]+', t)
        words.extend(found)
        
    return {
        "name": cat["name"],
        "titles": titles,
        "keywords": Counter(words).most_common(10)
    }

def main():
    print("=== Top 10 Titles Analysis ===")
    results = {}
    for cat in CATS:
        res = analyze_category_titles(cat)
        if res:
            results[cat["name"]] = res
            print(f"\n[{res['name']}]")
            for idx, t in enumerate(res["titles"]):
                print(f"  {idx+1}. {t}")
            print("  Top Words:", [f"{k}({v})" for k, v in res["keywords"][:6]])

if __name__ == "__main__":
    main()
