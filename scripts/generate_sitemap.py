import os
import yaml
import re
import urllib.parse

DOCS_DIR = "docs"
SITEMAP_FILE = "docs/Sitemap.md"
PAGES_FILE = "docs/.pages"
EXCLUDE_DIRS = {".pages", "javascripts", "stylesheets", "assets"}
EXCLUDE_FILES = {"index.md", "Recent_Changes.md", "Sitemap.md", ".pages"}

def get_title(filepath):
    """파일의 첫 번째 H1 제목을 가져옴"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith("# "): 
                    return line.strip("# ").strip()
    except:
        pass
    return os.path.basename(filepath)

def get_nav_order():
    """docs/.pages 파일에서 네비게이션 순서를 가져옴"""
    try:
        if not os.path.exists(PAGES_FILE):
            return []
        with open(PAGES_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            nav = data.get('nav', [])
            order = []
            for item in nav:
                if isinstance(item, str):
                    if item.endswith('.md'): continue
                    order.append(item)
                elif isinstance(item, dict):
                    label = list(item.keys())[0]
                    path = item[label]
                    if isinstance(path, str) and not path.endswith('.md'):
                        order.append(path)
                    else:
                        order.append(label)
            return order
    except Exception as e:
        print(f"⚠️ Failed to read nav order: {e}")
        return []

def build_troubleshooting_tree(dir_path):
    """Troubleshooting README.md에서 링크를 추출하여 목차 구성 (Sitemap용)"""
    text = ""
    readme_path = os.path.join(dir_path, "README.md")
    
    # 1. 기본 README 링크
    rel_readme = os.path.relpath(readme_path, DOCS_DIR)
    safe_readme = rel_readme.replace(os.sep, '/')
    text += f"* [{get_title(readme_path)}]({safe_readme})\n"
    
    # 2. README.md 내용 분석하여 링크 추출
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # [제목](경로) 형식 추출
                    match = re.search(r'\[([^\\]+)\]\(([^)]+\.md)\)', line)
                    if match:
                        title = match.group(1)
                        link = match.group(2)
                        
                        # 절대 경로로 변환 후 다시 상대 경로로 계산
                        target_path = os.path.normpath(os.path.join(dir_path, link))
                        rel_link = os.path.relpath(target_path, DOCS_DIR)
                        safe_link = rel_link.replace(os.sep, '/')
                        text += f"    * [{title}]({safe_link})\n"
        except Exception as e:
            print(f"⚠️ Error parsing Troubleshooting README for Sitemap: {e}")
            
    return text

def generate_sitemap():
    content = ["# 📚 TIL 전체 문서 목차\n", "\n", "모든 기술 지식을 한눈에 확인하고 바로 이동할 수 있습니다.\n", "\n"]
    
    existing_categories = [d for d in os.listdir(DOCS_DIR) if os.path.isdir(os.path.join(DOCS_DIR, d)) and d not in EXCLUDE_DIRS]
    nav_order = get_nav_order()
    
    sorted_categories = []
    for nav_item in nav_order:
        if nav_item in existing_categories:
            sorted_categories.append(nav_item)
            existing_categories.remove(nav_item)
    
    sorted_categories.extend(sorted(existing_categories))
    
    for cat in sorted_categories:
        content.append(f"## 📁 {cat}\n")
        content.append("\n")
        cat_path = os.path.join(DOCS_DIR, cat)
        
        if cat == "Troubleshooting":
            content.append(build_troubleshooting_tree(cat_path))
        else:
            for root, dirs, files in os.walk(cat_path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                level = root.replace(DOCS_DIR, "").count(os.sep) - 1
                indent = "    " * level
                
                if root != cat_path:
                    content.append(f"{indent}* **{os.path.basename(root)}**\n")
                    indent += "    "
                
                sorted_files = sorted(files)
                if "README.md" in sorted_files:
                    sorted_files.remove("README.md")
                    sorted_files.insert(0, "README.md")
                    
                for file in sorted_files:
                    if file.endswith(".md") and file not in EXCLUDE_FILES:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, DOCS_DIR)
                        safe_link = rel_path.replace(os.sep, '/')
                        title = get_title(file_path)
                        content.append(f"{indent}* [{title}]({safe_link})\n")
        
        content.append("\n")

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.writelines(content)
    
    print(f"✅ Successfully generated {SITEMAP_FILE}")

if __name__ == "__main__":
    generate_sitemap()
