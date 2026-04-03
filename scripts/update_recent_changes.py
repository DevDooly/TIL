import subprocess
import os
import re
import urllib.parse

RECENT_CHANGES_FILE = "docs/Recent_Changes.md"
README_FILE = "README.md"
DOCS_DIR = "docs"

# 대분류 표시 순서
CATEGORY_ORDER = [
    "Language",
    "Web",
    "Infrastructure",
    "Data",
    "ComputerScience",
    "Troubleshooting",
    "AI",
    "Tools",
    "History",
    "Travel",
    "RealEstate",
    "Templates"
]

def get_git_log(limit=50):
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
            # chore 커밋은 최근 변경 사항 목록에서 제외
            if current_message.startswith("chore:"):
                continue
                
            file_path = line
            if file_path.startswith("docs/") and file_path.endswith(".md") and "Recent_Changes.md" not in file_path and "README.md" not in file_path:
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
        link_path = item['file_path'][5:] 
        # URL encode and ensure forward slashes
        encoded_path = urllib.parse.quote(link_path.replace(os.sep, '/'))
        
        safe_msg = item['message'].replace("|", "\|").replace("<", "&lt;").replace(">", "&gt;")
        content += f"| {item['date']} | [{link_path}]({encoded_path}) | {safe_msg} |\n"
            
    with open(RECENT_CHANGES_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {RECENT_CHANGES_FILE}")

def update_readme_recent(items, max_display=6):
    display_items = items[:max_display]
    
    new_content = "\n"
    new_content += "| 날짜 | 문서 | 설명 |\n"
    new_content += "| :--- | :--- | :--- |\n"
    
    for item in display_items:
        link_path = item['file_path']
        display_name = os.path.basename(link_path).replace(".md", "").replace("_", " ")
        
        # URL encode and ensure forward slashes
        encoded_path = urllib.parse.quote(link_path.replace(os.sep, '/'))
        
        safe_msg = item['message'].replace("|", "\|").replace("<", "&lt;").replace(">", "&gt;")
        
        if len(safe_msg) > 50:
            safe_msg = safe_msg[:50] + "..."
            
        new_content += f"| {item['date']} | [{display_name}]({encoded_path}) | {safe_msg} |\n"
    new_content += "\n"

    update_file_section(README_FILE, "RECENT_CHANGES", new_content)

def get_markdown_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('# '):
                    return line.strip()[2:].strip()
    except:
        pass
    return os.path.basename(filepath).replace(".md", "").replace("_", " ")

def generate_toc_content():
    content = ""
    
    # 1. 상단 요약 링크 생성
    content += "### 📂 Categories\n"
    for cat in CATEGORY_ORDER:
        content += f"- [**{cat}**](#{cat.lower()})\n"
    
    content += "\n---\n\n"

    # 2. 상세 트리 생성
    existing_dirs = set()
    
    for category in CATEGORY_ORDER:
        dir_path = os.path.join(DOCS_DIR, category)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            existing_dirs.add(category)
            content += f"## {category}\n"
            
            # Troubleshooting 카테고리인 경우 특별 처리
            if category == "Troubleshooting":
                content += build_troubleshooting_tree(dir_path, is_readme=True)
            else:
                content += build_directory_tree(dir_path, level=0)
            content += "\n"
            
    # 정의되지 않은 나머지 디렉토리 처리
    for item in sorted(os.listdir(DOCS_DIR)):
        if item in existing_dirs or item.startswith('.') or item in ["assets", "javascripts", "search", "stylesheets"]:
            continue
        
        dir_path = os.path.join(DOCS_DIR, item)
        if os.path.isdir(dir_path):
            content += f"## {item}\n"
            content += build_directory_tree(dir_path, level=0)
            content += "\n"
            
    return content

def build_troubleshooting_tree(dir_path, is_readme=True):
    """Troubleshooting README.md에서 링크를 추출하여 목차 구성"""
    text = ""
    readme_path = os.path.join(dir_path, "README.md")
    
    # 1. 기본 README 링크
    rel_readme = os.path.relpath(readme_path, os.path.dirname(README_FILE) if is_readme else DOCS_DIR)
    encoded_readme = urllib.parse.quote(rel_readme.replace(os.sep, '/'))
    text += f"* [**Overview**]({encoded_readme})\n"
    
    # 2. README.md 내용 분석하여 링크 추출
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                # [제목](경로) 형식 추출 (유연한 정규식)
                match = re.search(r'\[(.*?)\]\((.*?\.md)\)', line)
                if match:
                    title = match.group(1)
                    link = match.group(2)
                    
                    # 절대 경로로 변환 후 다시 상대 경로로 계산
                    target_path = os.path.normpath(os.path.join(dir_path, link))
                    rel_link = os.path.relpath(target_path, os.path.dirname(README_FILE) if is_readme else DOCS_DIR)
                    encoded_link = urllib.parse.quote(rel_link.replace(os.sep, '/'))
                    text += f"  * [{title}]({encoded_link})\n"
        except Exception as e:
            print(f"⚠️ Error parsing Troubleshooting README: {e}")
            
    return text

def build_directory_tree(root_path, level):
    text = ""
    indent = "  " * level
    
    items = sorted(os.listdir(root_path))
    
    files = []
    dirs = []
    
    for item in items:
        if item.startswith('.') or item == "assets":
            continue
            
        full_path = os.path.join(root_path, item)
        if os.path.isdir(full_path):
            dirs.append(item)
        elif item.endswith(".md") and item != "README.md" and item != ".pages":
            files.append(item)
            
    # README.md 확인
    readme_path = os.path.join(root_path, "README.md")
    if os.path.exists(readme_path):
        rel_path = os.path.relpath(readme_path, os.path.dirname(README_FILE))
        encoded_path = urllib.parse.quote(rel_path.replace(os.sep, '/'))
        text += f"{indent}* [**Overview**]({encoded_path})\n"

    for f in files:
        full_path = os.path.join(root_path, f)
        title = get_markdown_title(full_path)
        rel_path = os.path.relpath(full_path, os.path.dirname(README_FILE))
        encoded_path = urllib.parse.quote(rel_path.replace(os.sep, '/'))
        text += f"{indent}* [{title}]({encoded_path})\n"
        
    for d in dirs:
        text += f"{indent}* **{d}**\n"
        text += build_directory_tree(os.path.join(root_path, d), level + 1)
        
    return text

def update_file_section(filepath, marker_name, new_content):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        start_marker = f"<!-- {marker_name}_START -->"
        end_marker = f"<!-- {marker_name}_END -->"
        
        pattern = f"({start_marker})(.*?)({end_marker})"
        
        if re.search(pattern, content, re.DOTALL):
            updated_content = re.sub(
                pattern, 
                f"\\1{new_content}\\3", 
                content, 
                flags=re.DOTALL
            )
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Successfully updated section {marker_name} in {filepath}")
        else:
            print(f"Warning: Markers {marker_name} not found in {filepath}")
            
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")

def main():
    # 1. Recent Changes 처리
    lines = get_git_log(100)
    items = parse_log(lines, 50)
    
    update_recent_changes_md(items)
    update_readme_recent(items, 6) 
    
    # 2. TOC 처리
    toc_content = generate_toc_content()
    update_file_section(README_FILE, "TOC", "\n" + toc_content)

if __name__ == "__main__":
    main()
