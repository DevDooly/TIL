import os
import yaml

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
                if line.startswith("# "): 
                    return line.strip("# ").strip()
    except:
        pass
    return os.path.basename(filepath)

def get_nav_order():
    """docs/.pages 파일에서 네비게이션 순서를 가져옴"""
    try:
        with open(PAGES_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            nav = data.get('nav', [])
            order = []
            for item in nav:
                if isinstance(item, str):
                    if item.endswith('.md'): continue
                    order.append(item)
                elif isinstance(item, dict):
                    order.append(list(item.keys())[0])
            return order
    except Exception as e:
        print(f"⚠️ Failed to read nav order: {e}")
        return []

def generate_sitemap():
    content = ["# 📚 TIL 전체 문서 목차\n", "\n", "모든 기술 지식을 한눈에 확인하고 바로 이동할 수 있습니다.\n", "\n"]
    
    # 1. 실제 디렉토리 목록 수집
    existing_categories = [d for d in os.listdir(DOCS_DIR) if os.path.isdir(os.path.join(DOCS_DIR, d)) and d not in EXCLUDE_DIRS]
    
    # 2. .pages 기반 순서 정렬
    nav_order = get_nav_order()
    
    sorted_categories = []
    for nav_item in nav_order:
        if nav_item in existing_categories:
            sorted_categories.append(nav_item)
            existing_categories.remove(nav_item)
    
    sorted_categories.extend(sorted(existing_categories))
    
    # 3. 목차 생성
    for cat in sorted_categories:
        content.append(f"## 📁 {cat}\n")
        content.append("\n")
        cat_path = os.path.join(DOCS_DIR, cat)
        
        for root, dirs, files in os.walk(cat_path):
            level = root.replace(DOCS_DIR, "").count(os.sep) - 1
            indent = "    " * level
            
            if root != cat_path:
                content.append(f"{indent}*   **{os.path.basename(root)}**\n")
                indent += "    "
            
            for file in sorted(files):
                if file.endswith(".md") and file not in EXCLUDE_FILES:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, DOCS_DIR)
                    title = get_title(file_path)
                    content.append(f"{indent}*   [{title}]({rel_path})\n")
        
        content.append("\n")

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.writelines(content)
    
    print(f"✅ Successfully generated {SITEMAP_FILE}")

if __name__ == "__main__":
    generate_sitemap()