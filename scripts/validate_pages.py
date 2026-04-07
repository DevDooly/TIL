import os
import yaml
import sys

DOCS_DIR = "docs"
EXIT_CODE = 0

def fix_path_string(path):
    """문자열 경로에서 후행 슬래시 제거"""
    if path.endswith("/"):
        return path[:-1], True
    return path, False

def traverse_and_fix(data, base_dir):
    """
    데이터 구조(List/Dict)를 순회하며 후행 슬래시를 제거하고,
    수정된 경로가 실제로 존재하는지 검증합니다.
    """
    global EXIT_CODE
    modified = False

    if isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, str):
                new_val, changed = fix_path_string(item)
                if changed:
                    print(f"🔧 Fixed: Removed trailing slash from '{item}' -> '{new_val}'")
                    data[i] = new_val
                    modified = True
                validate_path(base_dir, data[i])
            elif isinstance(item, dict):
                if traverse_and_fix(item, base_dir):
                    modified = True
                    
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                new_val, changed = fix_path_string(value)
                if changed:
                    print(f"🔧 Fixed: Removed trailing slash from '{value}' -> '{new_val}'")
                    data[key] = new_val
                    modified = True
                validate_path(base_dir, data[key])
            elif isinstance(value, (list, dict)):
                if traverse_and_fix(value, base_dir):
                    modified = True
    
    return modified

def validate_path(base_dir, path):
    """경로가 실제로 존재하는지 확인 (슬래시 시작시 docs 루트 기준)"""
    global EXIT_CODE
    if path.startswith("/"):
        full_path = os.path.join(DOCS_DIR, path[1:])
    else:
        full_path = os.path.join(base_dir, path)
        
    if not os.path.exists(full_path):
        print(f"❌ Error in {base_dir}: '{path}' does not exist.")
        EXIT_CODE = 1

def process_pages_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not data or 'nav' not in data:
            return

        base_dir = os.path.dirname(filepath)
        nav = data['nav']
        
        # 순회하며 수정 및 검증
        if traverse_and_fix(nav, base_dir):
            # 변경사항이 있으면 파일 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                # default_flow_style=False: 리스트를 블록 스타일로 유지
                # allow_unicode=True: 한글 깨짐 방지
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"💾 Saved changes to {filepath}")
            
    except Exception as e:
        print(f"⚠️ Failed to parse or process {filepath}: {e}")

def main():
    print("🔍 Validating and Fixing .pages files...")
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file == ".pages":
                process_pages_file(os.path.join(root, file))
    
    if EXIT_CODE == 0:
        print("✅ All .pages files are valid.")
    else:
        print("❌ Validation failed.")
        sys.exit(EXIT_CODE)

if __name__ == "__main__":
    main()