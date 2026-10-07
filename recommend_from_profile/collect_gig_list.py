import requests
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Origin": "https://kmong.com",
    "Referer": "https://kmong.com/category/668"
}

all_gigs = []
page = 1
per_page = 50

while True:
    url = f"https://api.kmong.com/gig-app/category/v1/categories/668/gigs?page={page}&perPage={per_page}&sort=RANKING"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Failed page {page}: {r.status_code}")
        break
    data = r.json()
    items = data.get("items", [])
    if not items:
        break
    all_gigs.extend(items)
    print(f"Page {page}/{data.get('lastPage')}: collected {len(items)} items, total so far {len(all_gigs)}")
    if page >= data.get("lastPage", 1):
        break
    page += 1
    time.sleep(0.3)

print(f"Total collected gigs: {len(all_gigs)}")
with open("c:/workspace/kmong/recommend_from_profile/gigs_list_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_gigs, f, ensure_ascii=False, indent=2)
print("Saved to gigs_list_raw.json")
