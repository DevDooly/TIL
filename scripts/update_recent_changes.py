import subprocess
import os

OUTPUT_FILE = "docs/Recent_Changes.md"

def get_git_log():
    # 최근 50개 커밋을 조회
    cmd = [
        "git", "log", "-n", "50",
        "--name-only",
        "--pretty=format:COMMIT_START|%ad|%s",
        "--date=format:%Y-%m-%d %H:%M"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result.stdout.splitlines()

def main():
    lines = get_git_log()
    
    content = "# 🕒 최근 변경 사항 (Recent Changes)\n\n"
    content += "최근 업데이트된 문서 목록입니다.\n\n"
    content += "| 수정 날짜 | 문서 경로 | 커밋 메시지 |\n"
    content += "| :--- | :--- | :--- |\n"
    
    current_date = ""
    current_message = ""
    
    row_count = 0
    max_rows = 50
    
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
                # 링크 생성을 위해 docs/ 접두사 제거
                link_path = file_path[5:] 
                
                # 메시지 내의 마크다운 문자 이스케이프 (파이프 등)
                safe_msg = current_message.replace("|", "\|").replace("<", "&lt;").replace(">", "&gt;")
                
                # 테이블 행 추가
                content += f"| {current_date} | [{link_path}]({link_path}) | {safe_msg} |\n"
                row_count += 1
        
        if row_count >= max_rows:
            break
            
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
