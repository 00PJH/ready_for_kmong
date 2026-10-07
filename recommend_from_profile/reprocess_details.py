import json

with open("c:/workspace/kmong/recommend_from_profile/gigs_list_raw.json", "r", encoding="utf-8") as f:
    raw_list = json.load(f)

raw_map = {g["gigId"]: g for g in raw_list}

with open("c:/workspace/kmong/recommend_from_profile/gigs_details_full.json", "r", encoding="utf-8") as f:
    details = json.load(f)

updated_count = 0
for d in details:
    gig_id = d["gigId"]
    raw = raw_map.get(gig_id)
    if raw:
        rev = raw.get("review", {})
        d["review_count"] = rev.get("reviewCount", 0)
        d["rating_score"] = rev.get("reviewAverage", 0.0)
        d["weighted_score"] = round(d["review_count"] * d["rating_score"], 2)
        d["ranking_order"] = raw.get("ranking_order", d.get("ranking_order", 0))
        d["advertisement_type"] = raw.get("advertisementType")
        d["is_ad"] = bool(raw.get("advertisementType"))
        d["is_prime"] = raw.get("isPrime", False)
        d["seller_grade"] = raw.get("seller", {}).get("grade", "")
        updated_count += 1

with open("c:/workspace/kmong/recommend_from_profile/gigs_details_full.json", "w", encoding="utf-8") as f:
    json.dump(details, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_count} items with correct review and ranking metrics.")
