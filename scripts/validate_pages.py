import os
import yaml
import sys

DOCS_DIR = "docs"
EXIT_CODE = 0

def validate_path(base_dir, path):
    # Handle absolute paths (relative to docs root) if needed, 
    # but .pages usually uses relative paths.
    
    # Remove trailing slash for existence check
    check_path = path
    if check_path.endswith("/"):
        check_path = check_path[:-1]
    
    full_path = os.path.join(base_dir, check_path)
    
    if not os.path.exists(full_path):
        return False
    return True

def validate_nav_item(base_dir, item):
    global EXIT_CODE
    
    if isinstance(item, str):
        # Just a filename or directory name
        if not validate_path(base_dir, item):
            print(f"❌ Error in {base_dir}: '{item}' does not exist.")
            EXIT_CODE = 1
    elif isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, str):
                if not validate_path(base_dir, value):
                    print(f"❌ Error in {base_dir} (Key: {key}): '{value}' does not exist.")
                    EXIT_CODE = 1
            elif isinstance(value, list):
                # Nested list
                for sub_item in value:
                    validate_nav_item(base_dir, sub_item)

def process_pages_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not data or 'nav' not in data:
            return

        base_dir = os.path.dirname(filepath)
        nav = data['nav']
        
        for item in nav:
            validate_nav_item(base_dir, item)
            
    except Exception as e:
        print(f"⚠️ Failed to parse {filepath}: {e}")

def main():
    print("🔍 Validating .pages files...")
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
