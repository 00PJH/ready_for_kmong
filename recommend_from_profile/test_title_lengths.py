titles = {
    "cat_667": [
        "ChatGPT 연동 사내문서·상담 맞춤 AI 챗봇 제작",
        "ChatGPT 연동 고객상담 사내문서 맞춤 AI 챗봇",
        "ChatGPT 연동 사내문서·상담 맞춤 AI 챗봇 개발",
        "ChatGPT 연동 사내문서 고객상담 맞춤 AI 챗봇"
    ],
    "cat_668": [
        "웹 크롤링·데이터 수집 맞춤 AI 업무 자동화 개발",
        "웹 크롤링 데이터 수집 및 맞춤 AI 자동화 프로그램",
        "웹 크롤링 데이터 수집 맞춤 AI 자동화 프로그램 개발",
        "웹 크롤링·데이터 수집 맞춤 AI 자동화 프로그램"
    ],
    "cat_670": [
        "YOLO 객체탐지·영상처리 및 맞춤 AI 음성인식 개발",
        "YOLO 영상처리·객체탐지 및 맞춤형 음성 AI 개발",
        "YOLO 객체탐지 영상처리 및 음성인식 AI 맞춤 개발",
        "YOLO 객체탐지·영상처리 및 맞춤 음성인식 개발"
    ]
}

for cat, t_list in titles.items():
    print(f"=== {cat} ===")
    for t in t_list:
        valid = "PASS (<=30)" if len(t) <= 30 else f"FAIL (>30, {len(t)})"
        print(f"[{len(t)}자] {valid}: {t}")
