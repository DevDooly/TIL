import subprocess
import os
import re

RECENT_CHANGES_FILE = "docs/Recent_Changes.md"
README_FILE = "README.md"

def get_git_log(limit=50):
    # 최근 n개 커밋을 조회
    cmd = [
        "git", "log", "-n", str(limit),
        "--name-only",
        "--pretty=format:COMMIT_START|%ad|%s",
        "--date=format:%Y-%m-%d %H:%M"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result.stdout.splitlines()

def parse_log(lines, max_items=50):
    parsed_items = []
    current_date = ""
    current_message = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("COMMIT_START|"):
            parts = line.split("|", 2)
            current_date = parts[1]
            current_message = parts[2]
        else:
            # 파일 경로 라인
            file_path = line
            # docs/ 폴더 내의 md 파일만 대상으로 함 (Recent_Changes.md 제외)
            if file_path.startswith("docs/") and file_path.endswith(".md") and "Recent_Changes.md" not in file_path:
                parsed_items.append({
                    "date": current_date,
                    "file_path": file_path,
                    "message": current_message
                })
                if len(parsed_items) >= max_items:
                    break
    return parsed_items

def update_recent_changes_md(items):
    content = "# 🕒 최근 변경 사항 (Recent Changes)\n\n"
    content += "최근 업데이트된 문서 목록입니다.\n\n"
    content += "| 수정 날짜 | 문서 경로 | 커밋 메시지 |\n"
    content += "| :--- | :--- | :--- |\n"
    
    for item in items:
        link_path = item['file_path'][5:] # docs/ 제거
        safe_msg = item['message'].replace("|", "\|").replace("<", "&lt;").replace(">", "&gt;")
        content += f"| {item['date']} | [{link_path}]({link_path}) | {safe_msg} |\n"
            
    with open(RECENT_CHANGES_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {RECENT_CHANGES_FILE}")

def update_readme_md(items, max_display=10):
    # README에는 상위 n개만 표시
    display_items = items[:max_display]
    
    new_content = "\n"
    new_content += "| 날짜 | 문서 | 설명 |\n"
    new_content += "| :--- | :--- | :--- |\n"
    
    for item in display_items:
        # README에서는 docs/ 부터 전체 경로 사용하거나 상대 경로 조정 필요
        # README.md 위치 기준 docs/는 올바른 상대 경로임
        link_path = item['file_path']
        display_name = os.path.basename(link_path).replace(".md", "").replace("_", " ")
        safe_msg = item['message'].replace("|", "\|").replace("<", "&lt;").replace(">", "&gt;")
        
        # 커밋 메시지가 너무 길면 자르기
        if len(safe_msg) > 50:
            safe_msg = safe_msg[:50] + "..."
            
        new_content += f"| {item['date']} | [{display_name}]({link_path}) | {safe_msg} |\n"
    new_content += "\n"

    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme_content = f.read()
        
        # 정규표현식으로 마커 사이 교체
        pattern = r"(<!-- RECENT_CHANGES_START -->)(.*?)(<!-- RECENT_CHANGES_END -->)"
        
        # re.DOTALL: .이 개행 문자를 포함하도록 설정
        if re.search(pattern, readme_content, re.DOTALL):
            updated_content = re.sub(
                pattern, 
                f"\\1{new_content}\\3", 
                readme_content, 
                flags=re.DOTALL
            )
            
            with open(README_FILE, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Successfully updated {README_FILE}")
        else:
            print(f"Warning: Markers not found in {README_FILE}")
            
    except FileNotFoundError:
        print(f"Error: {README_FILE} not found.")

def main():
    lines = get_git_log(100) # 충분히 가져옴
    items = parse_log(lines, 50) # 최대 50개 파싱
    
    update_recent_changes_md(items)
    update_readme_md(items, 10) # README에는 10개만

if __name__ == "__main__":
    main()