import requests
import json

url = "https://api.kmong.com/gig-app/gig/v1/gigs/795325/detail-modules?is_money_plus_path=false&clientType=DESKTOP"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Origin": "https://kmong.com",
    "Referer": "https://kmong.com/gig/795325"
}

r = requests.get(url, headers=headers)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Top-level keys:", data.keys() if isinstance(data, dict) else "List length: " + str(len(data)))
    if isinstance(data, dict):
        for k in data.keys():
            val = data[k]
            if isinstance(val, list):
                print(f"Key: {k}, list len: {len(val)}")
            elif isinstance(val, dict):
                print(f"Key: {k}, subkeys: {list(val.keys())[:5]}")
            else:
                print(f"Key: {k}, val preview: {str(val)[:100]}")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            print(f"Module {idx}:", item.get('type') if isinstance(item, dict) else type(item))
