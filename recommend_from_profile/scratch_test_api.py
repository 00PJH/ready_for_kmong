import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://kmong.com/category/668"
}

# Test possible API endpoints
test_urls = [
    "https://kmong.com/api/v1/categories/668/gigs",
    "https://kmong.com/api/categories/668",
    "https://kmong.com/_next/data/category/668.json",
    "https://api.kmong.com/v1/categories/668/gigs",
    "https://kmong.com/category/668?page=1"
]

for url in test_urls:
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"URL: {url} -> Status: {r.status_code}, Length: {len(r.text)}")
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
