import os
import yaml

DOCS_DIR = "docs"

def fix_pages_syntax():
    """PyYAML을 사용하여 .pages 파일의 문법과 인덴트를 표준화합니다."""
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file == ".pages":
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    
                    if data:
                        # 다시 덤프하여 인덴트와 문법을 표준화
                        with open(filepath, 'w', encoding='utf-8') as f:
                            yaml.dump(data, f, allow_unicode=True, sort_keys=False, indent=2, default_flow_style=False)
                        print(f"✅ Standardized: {filepath}")
                except Exception as e:
                    print(f"❌ Failed to fix {filepath}: {e}")

if __name__ == "__main__":
    fix_pages_syntax()