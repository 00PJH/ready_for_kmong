import re

allowed_specials = set(":+-#/.()")

titles = {
    "cat_667": "ChatGPT 연동 사내문서/상담 맞춤 AI 챗봇 제작",
    "cat_668": "웹 크롤링/데이터 수집 맞춤 AI 업무 자동화 개발",
    "cat_670": "YOLO 객체탐지/영상처리 및 맞춤 AI 음성인식 개발"
}

for cat, t in titles.items():
    length = len(t)
    specials = set(re.findall(r"[^0-9a-zA-Z가-힣\s]", t))
    invalid = specials - allowed_specials
    is_valid_len = 10 <= length <= 30
    is_valid_chars = len(invalid) == 0
    print(f"[{cat}] {length}자 | 길이적합: {is_valid_len} | 특수문자적합: {is_valid_chars} (특수문자: {specials}, 위반: {invalid}) -> {t}")
