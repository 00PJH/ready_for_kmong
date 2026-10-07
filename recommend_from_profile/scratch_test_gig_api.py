import requests
import json

url = "https://api.kmong.com/gig-app/category/v1/categories/668/gigs?page=1&perPage=10&sort=RANKING"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Origin": "https://kmong.com",
    "Referer": "https://kmong.com/"
}

r = requests.get(url, headers=headers)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Keys:", data.keys())
    # check pagination / total count
    print("Pagination info:", {k: v for k, v in data.items() if k != 'items' and k != 'gigs'})
    items = data.get('items') or data.get('gigs') or []
    print("Num items:", len(items))
    if items:
        first = items[0]
        print("First item keys:", first.keys())
        print("First item sample:", json.dumps(first, ensure_ascii=False, indent=2)[:500])
