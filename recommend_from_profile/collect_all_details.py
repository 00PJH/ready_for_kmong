import json
import os
import re
import time
import asyncio
import httpx
from bs4 import BeautifulSoup

RAW_LIST_PATH = "c:/workspace/kmong/recommend_from_profile/gigs_list_raw.json"
OUTPUT_PATH = "c:/workspace/kmong/recommend_from_profile/gigs_details_full.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Origin": "https://kmong.com",
    "Referer": "https://kmong.com/"
}

def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    # Replace br and p with newlines
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for p in soup.find_all("p"):
        p.append("\n")
    text = soup.get_text()
    # Normalize multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text

def parse_detail_modules(data, basic_info):
    parsed = {
        "gigId": basic_info.get("gigId"),
        "ranking_order": basic_info.get("ranking_order"),
        "title": basic_info.get("title"),
        "category_id": basic_info.get("currentCategoryId"),
        "url": f"https://kmong.com/gig/{basic_info.get('gigId')}",
        "advertisement_type": basic_info.get("advertisementType"),
        "is_ad": bool(basic_info.get("advertisementType")),
        "is_prime": basic_info.get("isPrime", False),
        "is_quality_guaranteed": basic_info.get("isQualityGuaranteed", False),
        
        # Seller Info
        "seller_nickname": basic_info.get("seller", {}).get("nickname", ""),
        "seller_grade": basic_info.get("seller", {}).get("grade", ""),
        "seller_id": basic_info.get("seller", {}).get("userId"),
        "seller_intro": "",
        "avg_response_time": "",
        
        # Performance / Reviews
        "review_count": basic_info.get("review", {}).get("count", 0) if basic_info.get("review") else 0,
        "rating_score": basic_info.get("review", {}).get("score", 0.0) if basic_info.get("review") else 0.0,
        
        # Base Price
        "base_price": basic_info.get("price", 0),
        
        # Description sections
        "description": "",
        "service_process": "",
        "buyer_preparation": "",
        "revision_policy": "",
        
        # Metadata
        "ai_tools": [],
        "tech_level": "",
        "team_size": "",
        "work_location": "",
        "metadata_raw": [],
        
        # Packages
        "packages": {
            "STANDARD": {},
            "DELUXE": {},
            "PREMIUM": {}
        }
    }
    
    # Check COMMON
    common = data.get("COMMON", {})
    if common:
        user_info = common.get("user", {})
        parsed["avg_response_time"] = user_info.get("avg_response_time", "")
    
    # Check LEFT modules
    for item in data.get("LEFT", []):
        title = item.get("title", "")
        desc = item.get("description", "")
        
        if title == "서비스 설명" and desc:
            parsed["description"] = clean_html(desc)
        elif title == "서비스 제공 절차" and desc:
            parsed["service_process"] = clean_html(desc)
        elif title == "의뢰인 준비사항" and desc:
            parsed["buyer_preparation"] = clean_html(desc)
        elif title == "수정 및 재진행" and desc:
            parsed["revision_policy"] = clean_html(desc)
            
        # Metadata
        if "metadata" in item and isinstance(item["metadata"], list):
            parsed["metadata_raw"] = item["metadata"]
            for m in item["metadata"]:
                m_title = m.get("title", "")
                m_meta = m.get("meta", [])
                if "AI 툴" in m_title:
                    parsed["ai_tools"] = m_meta
                elif "기술 수준" in m_title:
                    parsed["tech_level"] = ", ".join(m_meta)
                elif "팀 규모" in m_title:
                    parsed["team_size"] = ", ".join(m_meta)
                elif "상주" in m_title:
                    parsed["work_location"] = ", ".join(m_meta)
                    
        # Seller profile intro
        if "user" in item and isinstance(item["user"], dict):
            seller_intro = item["user"].get("intro", "")
            if seller_intro:
                parsed["seller_intro"] = clean_html(seller_intro)
                
    # Check RIGHT modules (packages)
    for item in data.get("RIGHT", []):
        if "packages" in item and isinstance(item["packages"], list):
            for pkg in item["packages"]:
                p_type = pkg.get("type", "").upper()
                if p_type in ["STANDARD", "DELUXE", "PREMIUM"]:
                    p_info = {
                        "title": pkg.get("title", ""),
                        "price": pkg.get("price", 0),
                        "description": pkg.get("description", ""),
                        "working_days": None,
                        "revision_count": None
                    }
                    for attr in pkg.get("attributes", []):
                        if attr.get("type") == "DAY":
                            p_info["working_days"] = attr.get("value")
                        elif attr.get("type") == "REVISION":
                            p_info["revision_count"] = attr.get("value")
                    parsed["packages"][p_type] = p_info

    return parsed

async def fetch_detail(client, semaphore, gig_item, idx, total, results):
    gig_id = gig_item["gigId"]
    url = f"https://api.kmong.com/gig-app/gig/v1/gigs/{gig_id}/detail-modules?is_money_plus_path=false&clientType=DESKTOP"
    
    async with semaphore:
        for attempt in range(3):
            try:
                r = await client.get(url, headers=HEADERS, timeout=12.0)
                if r.status_code == 200:
                    data = r.json()
                    parsed = parse_detail_modules(data, gig_item)
                    results.append(parsed)
                    if len(results) % 25 == 0 or len(results) == total:
                        print(f"Progress: {len(results)}/{total} ({(len(results)/total)*100:.1f}%) collected")
                    return
                elif r.status_code == 404:
                    print(f"Gig {gig_id} returned 404 (possibly deactivated)")
                    return
                else:
                    await asyncio.sleep(1.0 * (attempt + 1))
            except Exception as e:
                if attempt == 2:
                    print(f"Failed gig {gig_id}: {e}")
                await asyncio.sleep(1.0 * (attempt + 1))

async def main():
    with open(RAW_LIST_PATH, "r", encoding="utf-8") as f:
        gigs = json.load(f)
        
    for idx, g in enumerate(gigs):
        g["ranking_order"] = idx + 1
        
    print(f"Loaded {len(gigs)} raw gigs. Starting detailed module scraping...")
    
    semaphore = asyncio.Semaphore(6)  # 6 concurrent requests
    results = []
    
    limits = httpx.Limits(max_keepalive_connections=15, max_connections=20)
    async with httpx.AsyncClient(limits=limits) as client:
        tasks = [
            fetch_detail(client, semaphore, g, idx, len(gigs), results)
            for idx, g in enumerate(gigs)
        ]
        await asyncio.gather(*tasks)
        
    print(f"Finished scraping! Total successful: {len(results)}/{len(gigs)}")
    
    # Sort results by original ranking order
    results.sort(key=lambda x: x["ranking_order"])
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved all detailed modules to {OUTPUT_PATH}")

if __name__ == "__main__":
    asyncio.run(main())
