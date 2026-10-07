import json

with open("c:/workspace/kmong/recommend_from_profile/gigs_list_raw.json", "r", encoding="utf-8") as f:
    gigs = json.load(f)

reviews = []
for g in gigs:
    rev = g.get("review", {})
    cnt = rev.get("reviewCount", 0)
    avg = rev.get("reviewAverage", 0.0)
    if cnt > 0:
        reviews.append({
            "gigId": g.get("gigId"),
            "title": g.get("title"),
            "seller": g.get("seller", {}).get("nickname"),
            "grade": g.get("seller", {}).get("grade"),
            "reviewCount": cnt,
            "reviewAverage": avg,
            "price": g.get("price")
        })

print(f"Total gigs: {len(gigs)}")
print(f"Gigs with reviewCount > 0: {len(reviews)}")
reviews.sort(key=lambda x: x["reviewCount"], reverse=True)
print("\nTop 15 gigs by reviewCount:")
for r in reviews[:15]:
    print(r)
