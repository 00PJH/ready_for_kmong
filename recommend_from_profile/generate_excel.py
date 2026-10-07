import json
import re
import pandas as pd
import openpyxl
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

JSON_PATH = "c:/workspace/kmong/recommend_from_profile/gigs_details_full.json"
EXCEL_OUTPUT_ROOT = "c:/workspace/kmong/kmong_ai_automation_services_564.xlsx"
EXCEL_OUTPUT_REC = "c:/workspace/kmong/recommend_from_profile/kmong_ai_automation_services_564.xlsx"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    items = json.load(f)

def clean_excel_text(val):
    if isinstance(val, str):
        return ILLEGAL_CHARACTERS_RE.sub('', val)
    return val

def flatten_item(item):
    pkg_std = item.get("packages", {}).get("STANDARD", {})
    pkg_dlx = item.get("packages", {}).get("DELUXE", {})
    pkg_prm = item.get("packages", {}).get("PREMIUM", {})
    
    ai_tools_str = ", ".join(item.get("ai_tools", [])) if item.get("ai_tools") else ""
    
    row = {
        "순번": item.get("ranking_order"),
        "서비스ID": item.get("gigId"),
        "서비스명": item.get("title"),
        "크몽랭킹": item.get("ranking_order"),
        "광고여부": "광고(CPC)" if item.get("is_ad") else "일반",
        "프라임여부": "PRIME" if item.get("is_prime") else "일반",
        "품질보증": "보증" if item.get("is_quality_guaranteed") else "-",
        "판매자닉네임": item.get("seller_nickname"),
        "판매자등급": item.get("seller_grade"),
        "응답시간": item.get("avg_response_time"),
        "대표시작가(원)": item.get("base_price"),
        "누적리뷰수": item.get("review_count"),
        "평점": item.get("rating_score"),
        "실적가중스코어": item.get("weighted_score"),
        
        # STANDARD
        "STD_상품명": pkg_std.get("title", ""),
        "STD_가격(원)": pkg_std.get("price", ""),
        "STD_작업일": pkg_std.get("working_days", ""),
        "STD_수정횟수": pkg_std.get("revision_count", ""),
        "STD_설명": pkg_std.get("description", ""),
        
        # DELUXE
        "DLX_상품명": pkg_dlx.get("title", ""),
        "DLX_가격(원)": pkg_dlx.get("price", ""),
        "DLX_작업일": pkg_dlx.get("working_days", ""),
        "DLX_수정횟수": pkg_dlx.get("revision_count", ""),
        "DLX_설명": pkg_dlx.get("description", ""),
        
        # PREMIUM
        "PRM_상품명": pkg_prm.get("title", ""),
        "PRM_가격(원)": pkg_prm.get("price", ""),
        "PRM_작업일": pkg_prm.get("working_days", ""),
        "PRM_수정횟수": pkg_prm.get("revision_count", ""),
        "PRM_설명": pkg_prm.get("description", ""),
        
        # Metadata
        "사용AI툴": ai_tools_str,
        "기술수준": item.get("tech_level", ""),
        "팀규모": item.get("team_size", ""),
        "상주여부": item.get("work_location", ""),
        
        # Descriptions
        "서비스설명_전문": item.get("description", ""),
        "서비스제공절차": item.get("service_process", ""),
        "의뢰인준비사항": item.get("buyer_preparation", ""),
        "수정및재진행규정": item.get("revision_policy", ""),
        "판매자소개": item.get("seller_intro", ""),
        "서비스URL": item.get("url")
    }
    return {k: clean_excel_text(v) for k, v in row.items()}

flat_data = [flatten_item(it) for it in items]
df_all = pd.DataFrame(flat_data)

# Option A: Sort by review_count desc, rating_score desc, base_price desc
df_option_a = df_all.sort_values(by=["누적리뷰수", "평점", "대표시작가(원)"], ascending=[False, False, False]).head(100).copy()
df_option_a.reset_index(drop=True, inplace=True)
df_option_a.insert(0, "실적순위", range(1, len(df_option_a) + 1))

# Option B: Sort by 크몽랭킹 asc
df_option_b = df_all.sort_values(by="크몽랭킹", ascending=True).head(100).copy()
df_option_b.reset_index(drop=True, inplace=True)
df_option_b.insert(0, "노출순위", range(1, len(df_option_b) + 1))

# Option C: Hybrid - Top 50 by Ranking + Top 50 by Review Count (deduplicated)
top_50_ranking = df_all.sort_values(by="크몽랭킹", ascending=True).head(50)
seen_ids = set(top_50_ranking["서비스ID"])

top_reviews_candidates = df_all.sort_values(by=["누적리뷰수", "평점", "대표시작가(원)"], ascending=[False, False, False])
hybrid_items = list(top_50_ranking.to_dict('records'))

for _, row in top_reviews_candidates.iterrows():
    if len(hybrid_items) >= 100:
        break
    if row["서비스ID"] not in seen_ids:
        seen_ids.add(row["서비스ID"])
        hybrid_items.append(row.to_dict())

df_option_c = pd.DataFrame(hybrid_items)
df_option_c.insert(0, "하이브리드순위", range(1, len(df_option_c) + 1))

print("DataFrames prepared:")
print(f"- All: {len(df_all)}")
print(f"- Option A: {len(df_option_a)}")
print(f"- Option B: {len(df_option_b)}")
print(f"- Option C: {len(df_option_c)}")

def style_worksheet(ws, header_color="1F497D"):
    header_font = Font(name="Pretendard", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color=header_color, end_color=header_color, fill_type="solid")
    regular_font = Font(name="Pretendard", size=10)
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    ws.freeze_panes = "D2"
    
    # Header styling
    for col_num in range(1, ws.max_column + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=False)
        cell.border = thin_border
    
    # Rows styling
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.font = regular_font
            cell.border = thin_border
            header_val = ws.cell(row=1, column=cell.column).value
            if header_val in ["순번", "서비스ID", "크몽랭킹", "실적순위", "노출순위", "하이브리드순위", "누적리뷰수", "평점", "실적가중스코어", "STD_작업일", "STD_수정횟수", "DLX_작업일", "DLX_수정횟수", "PRM_작업일", "PRM_수정횟수"]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif "가격" in str(header_val):
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '#,##0'
            elif "URL" in str(header_val):
                cell.alignment = Alignment(horizontal="left", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
    # Auto column width
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        header_val = str(col[0].value or "")
        if "설명" in header_val or "절차" in header_val or "준비" in header_val or "소개" in header_val or "규정" in header_val:
            ws.column_dimensions[col_letter].width = 30
        elif "URL" in header_val:
            ws.column_dimensions[col_letter].width = 25
        elif "서비스명" in header_val:
            ws.column_dimensions[col_letter].width = 35
        elif "상품명" in header_val:
            ws.column_dimensions[col_letter].width = 25
        else:
            max_len = max(len(str(cell.value or '')) for cell in col[:15])
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

# Write to both target paths
for target_excel in [EXCEL_OUTPUT_ROOT, EXCEL_OUTPUT_REC]:
    with pd.ExcelWriter(target_excel, engine="openpyxl") as writer:
        df_all.to_excel(writer, sheet_name="전체_서비스_563개", index=False)
        df_option_a.to_excel(writer, sheet_name="옵션A_실적우수_TOP100", index=False)
        df_option_b.to_excel(writer, sheet_name="옵션B_노출랭킹_TOP100", index=False)
        df_option_c.to_excel(writer, sheet_name="옵션C_하이브리드_TOP100", index=False)
        
    wb = openpyxl.load_workbook(target_excel)
    style_worksheet(wb["전체_서비스_563개"], "2C3E50")     # Navy
    style_worksheet(wb["옵션A_실적우수_TOP100"], "1B4F72")   # Dark Blue
    style_worksheet(wb["옵션B_노출랭킹_TOP100"], "1E8449")   # Green
    style_worksheet(wb["옵션C_하이브리드_TOP100"], "7D3C98") # Purple
    wb.save(target_excel)
    print(f"Successfully generated and styled Excel: {target_excel}")
