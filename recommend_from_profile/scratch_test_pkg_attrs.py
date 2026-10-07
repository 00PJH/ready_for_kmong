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
for item in data.get("RIGHT", []):
    if "packages" in item:
        for p in item["packages"]:
            print(f"--- Package: {p.get('type')} ({p.get('title')}) ---")
            print("Price:", p.get("price"))
            print("Description:", p.get("description"))
            print("Attributes:", json.dumps(p.get("attributes"), ensure_ascii=False))
