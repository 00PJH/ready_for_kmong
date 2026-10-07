import requests

categories = [
    (651, "AI 시스템·서비스"),
    (667, "맞춤형 챗봇·GPT"),
    (669, "프롬프트 설계(엔지니어링)"),
    (649, "AI 모델링·최적화"),
    (670, "이미지·음성 인식"),
    (672, "AI 기능 개발·연동"),
    (673, "AI 에이전트"),
    (674, "AI 데이터 분석"),
    (675, "AI 도입 컨설팅"),
    (676, "자연어 처리"),
    (648, "데이터 전처리·분석·시각화")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Origin": "https://kmong.com"
}

total_gigs_sum = 0
for cat_id, name in categories:
    url = f"https://api.kmong.com/gig-app/category/v1/categories/{cat_id}/gigs?page=1&perPage=50&sort=RANKING"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        count = data.get("totalItemCount", 0)
        pages = data.get("lastPage", 0)
        total_gigs_sum += count
        print(f"[{cat_id}] {name}: {count} gigs (pages: {pages})")
    else:
        print(f"[{cat_id}] {name}: Error {r.status_code}")

print(f"Total across all categories: {total_gigs_sum}")
