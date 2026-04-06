import os
import re

DOCS_DIR = "docs"

def quote_pages_labels():
    # 패턴: - Label: Value
    # Label 부분에 특수문자나 콜론이 있을 수 있으므로 따옴표로 감쌈
    # 이미 따옴표가 있는 경우는 무시
    pattern = re.compile(r'^(\s*-\s+)([^"\'].*?):\s*(.*)$')
    
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file == ".pages":
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                modified = False
                for line in lines:
                    match = pattern.match(line)
                    if match:
                        indent_dash = match.group(1)
                        label = match.group(2).strip()
                        value = match.group(3).strip()
                        
                        # 라벨에 콜론, &, (, ) 등 특수문자가 있거나 한글이 포함된 경우 안전하게 따옴표 추가
                        # (단, 디렉토리 이름만 있는 경우 등은 제외하되, 여기서는 일관성을 위해 웬만하면 감쌈)
                        new_line = f'{indent_dash}"{label}": {value}\n'
                        if new_line != line:
                            line = new_line
                            modified = True
                    new_lines.append(line)
                
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Quoted labels in: {filepath}")

if __name__ == "__main__":
    quote_pages_labels()
