import os

DOCS_DIR = "docs"
INDEX_FILE = "docs/index.md"
EXCLUDE_DIRS = {".pages", "javascripts", "stylesheets", "assets"}
EXCLUDE_FILES = {"index.md", "Recent_Changes.md", ".pages"}

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

def generate_sitemap():
    content = ["# 📚 TIL 전체 문서 목차\n", "\n", "모든 기술 지식을 한눈에 확인하고 바로 이동할 수 있습니다.\n", "\n"]
    
    # 최상위 카테고리 (docs 바로 아래 디렉토리들)
    categories = sorted([d for d in os.listdir(DOCS_DIR) if os.path.isdir(os.path.join(DOCS_DIR, d)) and d not in EXCLUDE_DIRS])
    
    for cat in categories:
        content.append(f"## 📁 {cat}\n")
        content.append("\n") # 헤더와 리스트 사이에 빈 줄 추가
        cat_path = os.path.join(DOCS_DIR, cat)
        
        # 하위 파일 및 디렉토리 탐색
        for root, dirs, files in os.walk(cat_path):
            level = root.replace(DOCS_DIR, "").count(os.sep) - 1
            indent = "    " * level
            
            # 현재 디렉토리 이름 표시 (최상위 카테고리 제외)
            if root != cat_path:
                content.append(f"{indent}*   **{os.path.basename(root)}**\n")
                indent += "    "
            
            # 파일 목록 (가나다순 정렬)
            for file in sorted(files):
                if file.endswith(".md") and file not in EXCLUDE_FILES:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, DOCS_DIR)
                    title = get_title(file_path)
                    content.append(f"{indent}*   [{title}]({rel_path})\n")
        
        content.append("\n")

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.writelines(content)
    
    print(f"✅ Successfully generated {INDEX_FILE}")

if __name__ == "__main__":
    generate_sitemap()