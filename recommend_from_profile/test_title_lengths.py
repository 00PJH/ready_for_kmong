import re

allowed = set(":+-#/.()")

titles = {
    "1순위 (챗봇)": "AI 연동 사내문서/고객상담 등 맞춤 챗봇 제작",
    "2순위 (자동화)": "웹 크롤링/데이터 수집 및 AI 요약/자동화 개발",
    "3순위 (비전음성)": "YOLO 객체탐지/관절 추출/음성인식 맞춤 AI 개발"
}

for k, t in titles.items():
    l = len(t)
    specials = set(re.findall(r"[^0-9a-zA-Z가-힣\s]", t))
    invalid = specials - allowed
    print(f"{k} [{l}자] | 길이(10~30): {10<=l<=30} | 특수문자(:+-#/.()): {len(invalid)==0} -> {t}")
