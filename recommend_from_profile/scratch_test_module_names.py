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
print("COMMON:", json.dumps(data.get("COMMON"), ensure_ascii=False, indent=2)[:400])

for sec in ['LEFT', 'RIGHT', 'BOTTOM']:
    print(f"\n--- {sec} ---")
    for item in data.get(sec, []):
        mod_name = item.get("module_name") or item.get("name") or list(item.keys())
        print("Module:", mod_name)
