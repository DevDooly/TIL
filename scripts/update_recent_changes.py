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

def get_git_log(limit=100):
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
            # docs 내의 마크다운 파일만 대상 (관리 파일 제외)
            if (file_path.startswith("docs/") and 
                file_path.endswith(".md") and 
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
        safe_msg = item['message'].replace("|", "\|").replace("<", "&lt;").replace(">", "&gt;")
        content += f"| {item['date']} | [{link_path}]({safe_link}) | {safe_msg} |\n"
            
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
        safe_link = link_path.replace(os.sep, '/')
        safe_msg = item['message'].replace("|", "\|").replace("<", "&lt;").replace(">", "&gt;")
        
        if len(safe_msg) > 50:
            safe_msg = safe_msg[:50] + "... "
            
        new_content += f"| {item['date']} | [{display_name}]({safe_link}) | {safe_msg} |\n"
    new_content += "\n"

    update_file_section(README_FILE, "RECENT_CHANGES", new_content)

def update_file_section(filepath, marker_name, new_content):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        start_marker = f"<!-- {marker_name}_START -->"
        end_marker = f"<!-- {marker_name}_END -->"
        pattern = f"({start_marker})(.*?)({end_marker})"
        
        if re.search(pattern, content, re.DOTALL):
            updated_content = re.sub(pattern, f"\\1{new_content}\\3", content, flags=re.DOTALL)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Successfully updated section {marker_name} in {filepath}")
    except Exception as e:
        print(f"Error updating {filepath}: {e}")

# ... (generate_toc_content 등 기존 함수 유지) ...

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
    content += "### 📂 Categories\n"
    for cat in CATEGORY_ORDER:
        content += f"- [**{cat}**](#{cat.lower()})\n"
    content += "\n---\n\n"

    existing_dirs = set()
    for category in CATEGORY_ORDER:
        dir_path = os.path.join(DOCS_DIR, category)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            existing_dirs.add(category)
            content += f"## {category}\n"
            if category == "Troubleshooting":
                content += build_troubleshooting_tree(dir_path)
            else:
                content += build_directory_tree(dir_path, level=0)
            content += "\n"
            
    for item in sorted(os.listdir(DOCS_DIR)):
        if item in existing_dirs or item.startswith('.') or item in ["assets", "javascripts", "search", "stylesheets"]:
            continue
        dir_path = os.path.join(DOCS_DIR, item)
        if os.path.isdir(dir_path):
            content += f"## {item}\n"
            content += build_directory_tree(dir_path, level=0)
            content += "\n"
    return content

def build_troubleshooting_tree(dir_path):
    text = ""
    readme_path = os.path.join(dir_path, "README.md")
    rel_path = os.path.relpath(readme_path, os.path.dirname(README_FILE))
    safe_path = rel_path.replace(os.sep, '/')
    text += f"* [**Overview**]({safe_path})\n"
    
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                for line in f:
                    match = re.search(r'\[(.*?)\]\((.*?\.md)\)', line)
                    if match:
                        title, link = match.group(1), match.group(2)
                        target_path = os.path.normpath(os.path.join(dir_path, link))
                        rel_link = os.path.relpath(target_path, os.path.dirname(README_FILE))
                        text += f"  * [{title}]({rel_link.replace(os.sep, '/')})\n"
        except: pass
    return text

def build_directory_tree(root_path, level):
    text = ""
    indent = "  " * level
    items = sorted(os.listdir(root_path))
    files, dirs = [], []
    for item in items:
        if item.startswith('.') or item == "assets": continue
        full_path = os.path.join(root_path, item)
        if os.path.isdir(full_path): dirs.append(item)
        elif item.endswith(".md") and item != "README.md" and item != ".pages": files.append(item)
            
    readme_path = os.path.join(root_path, "README.md")
    if os.path.exists(readme_path):
        rel_path = os.path.relpath(readme_path, os.path.dirname(README_FILE))
        text += f"{indent}* [**Overview**]({rel_path.replace(os.sep, '/')})\n"

    for f in files:
        full_path = os.path.join(root_path, f)
        rel_path = os.path.relpath(full_path, os.path.dirname(README_FILE))
        text += f"{indent}* [{get_markdown_title(full_path)}]({rel_path.replace(os.sep, '/')})\n"
    for d in dirs:
        text += f"{indent}* **{d}**\n"
        text += build_directory_tree(os.path.join(root_path, d), level + 1)
    return text

def main():
    lines = get_git_log(100)
    items = parse_log(lines, 50)
    update_recent_changes_md(items)
    update_readme_recent(items, 6) 
    toc_content = generate_toc_content()
    update_file_section(README_FILE, "TOC", "\n" + toc_content)

if __name__ == "__main__":
    main()