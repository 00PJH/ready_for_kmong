import requests
import json

url = "https://api.kmong.com/gig-app/gig/v1/gigs/795325/detail-modules?is_money_plus_path=false&clientType=DESKTOP"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Origin": "https://kmong.com",
    "Referer": "https://kmong.com/gig/795325"
}

r = requests.get(url, headers=headers)
data = r.json()

# Inspect packages
packages = []
for item in data.get("RIGHT", []):
    if "packages" in item:
        packages = item["packages"]
        break

print("Packages count:", len(packages))
for p in packages:
    print("Package keys:", p.keys())
    print("Package sample:", {k: p[k] for k in ['name', 'title', 'price', 'working_days', 'revision_count'] if k in p})

# Inspect description & metadata from LEFT
for idx, item in enumerate(data.get("LEFT", [])):
    if "description" in item:
        print(f"LEFT[{idx}] description keys:", item.keys())
        print(f"LEFT[{idx}] title:", item.get("title"))
        print(f"LEFT[{idx}] desc preview:", str(item.get("description"))[:200])
    if "metadata" in item:
        print(f"LEFT[{idx}] metadata:", json.dumps(item.get("metadata"), ensure_ascii=False)[:300])
