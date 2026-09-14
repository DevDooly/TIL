import subprocess
import os

RECENT_CHANGES_FILE = "docs/Recent_Changes.md"

def get_git_log(limit=100):
    cmd = [
        "git", "-c", "core.quotepath=false", "log", "-n", str(limit),
        "--name-only",
        "--pretty=format:COMMIT_START|%ad|%s",
        "--date=format:%Y-%m-%d %H:%M"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)
    return result.stdout.splitlines()

def parse_log(lines, max_items=50):
    parsed_items = []
    seen_files = set() # 중복 제거를 위한 세트
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
            file_path = line
            # docs 내의 마크다운 파일만 대상 (관리 파일 제외 및 실제 존재하는 파일만)
            if (file_path.startswith("docs/") and 
                file_path.endswith(".md") and 
                os.path.exists(file_path) and
                not any(x in file_path for x in ["Recent_Changes.md", "README.md", "Sitemap.md", "index.md"])):
                
                # 파일별로 가장 최근 수정 내역만 기록 (중복 제거)
                if file_path not in seen_files:
                    parsed_items.append({
                        "date": current_date,
                        "file_path": file_path,
                        "message": current_message
                    })
                    seen_files.add(file_path)
                    
                if len(parsed_items) >= max_items:
                    break
    return parsed_items

def update_recent_changes_md(items):
    content = "# 🕒 최근 변경 사항 (Recent Changes)\n\n"
    content += "최근 업데이트된 문서 목록입니다. (각 문서별 최신 수정 이력만 표시됩니다.)\n\n"
    content += "| 수정 날짜 | 문서 경로 | 커밋 메시지 |\n"
    content += "| :--- | :--- | :--- |\n"
    
    for item in items:
        link_path = item['file_path'][5:] 
        # MkDocs는 내부 링크 해결을 위해 파일 시스템의 실제 경로를 필요로 하므로 인코딩하지 않음
        safe_link = link_path.replace(os.sep, '/')
        safe_msg = item['message'].replace("|", r"\|").replace("<", "&lt;").replace(">", "&gt;")
        content += f"| {item['date']} | [{link_path}]({safe_link}) | {safe_msg} |\n"
            
    with open(RECENT_CHANGES_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {RECENT_CHANGES_FILE}")

def main():
    lines = get_git_log(100)
    items = parse_log(lines, 50)
    # README는 직접 관리하고, 상세 변경 이력은 전용 문서에만 생성한다.
    update_recent_changes_md(items)


if __name__ == "__main__":
    main()
