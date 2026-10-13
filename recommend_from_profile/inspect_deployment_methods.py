import json

def inspect_category(cat_path, cat_name):
    print(f"\n==========================================")
    print(f" CATEGORY: {cat_name} ({cat_path})")
    print(f"==========================================")
    with open(f"{cat_path}/gigs_details_full.json", "r", encoding="utf-8") as f:
        gigs = json.load(f)
    
    top_gigs = sorted(gigs, key=lambda x: (x.get("review_count", 0), x.get("rating_score", 0)), reverse=True)[:10]
    
    for i, g in enumerate(top_gigs, 1):
        nick = g.get("seller_nickname")
        title = g.get("title")
        revs = g.get("review_count")
        print(f"\n#{i} [{nick}] {title} (리뷰 {revs}건)")
        
        desc = g.get("description", "")
        proc = g.get("service_process", "")
        prep = g.get("buyer_preparation", "")
        
        # Look for delivery, deployment, framework mentions
        text = f"{desc}\n{proc}\n{prep}"
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        target_kws = ["배포", "호스팅", "서버", "streamlit", "vercel", "카카오", "도커", "docker", "위젯", "iframe", "클라우드", "aws", "카페24", "임베드", "exe", "소스코드", "인수인계", "html", "javascript", "react", "next", "fastapi", "flask", "langchain", "깃허브", "github"]
        hits = []
        for line in lines:
            if any(kw in line.lower() for kw in target_kws):
                hits.append(line)
        
        print("  [기술/배포/전달 관련 발췌]:")
        for h in hits[:6]:
            print(f"    * {h[:120]}")
            
        pkgs = g.get("packages", {})
        print("  [패키지 정보]:")
        if isinstance(pkgs, dict):
            for pname, pdata in pkgs.items():
                if isinstance(pdata, dict):
                    print(f"    - {pname}: {pdata.get('price', 0):,}원 / 작업 {pdata.get('working_days')}일 / 수정 {pdata.get('revision_count')}회 / 설명: {pdata.get('description')}")
        elif isinstance(pkgs, list):
            for p in pkgs:
                if isinstance(p, dict):
                    print(f"    - {p.get('name')}: {p.get('price', 0):,}원 / 작업 {p.get('working_days')}일 / 수정 {p.get('revision_count')}회 / 설명: {p.get('description')}")

if __name__ == "__main__":
    inspect_category("../맞춤형_챗봇_GPT", "맞춤형 챗봇·GPT (667)")
