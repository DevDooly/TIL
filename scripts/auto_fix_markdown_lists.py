import os
import re

DOCS_DIR = "docs"

def fix_markdown_lists():
    list_pattern = re.compile(r'^(\s*)([-*]|\d+\.)\s+(.*)')
    files_fixed = 0
    
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                in_code_block = False
                modified = False
                
                for i in range(len(lines)):
                    line = lines[i]
                    stripped = line.strip()
                    
                    if stripped.startswith("```"):
                        in_code_block = not in_code_block
                        new_lines.append(line)
                        continue
                    if in_code_block:
                        new_lines.append(line)
                        continue
                    
                    match = list_pattern.match(line)
                    if match:
                        # 리스트 항목인 경우
                        if i > 0:
                            prev_line_stripped = new_lines[-1].strip()
                            # 이전 줄이 비어있지 않고, 리스트도 아니면 빈 줄 추가
                            if prev_line_stripped and not list_pattern.match(new_lines[-1]):
                                if not prev_line_stripped.startswith('<!--') and prev_line_stripped != '---':
                                    new_lines.append("\n")
                                    modified = True
                        
                        # 불렛 뒤 공백 1개로 통일
                        indent = match.group(1)
                        marker = match.group(2)
                        content = match.group(3)
                        new_line = f"{indent}{marker} {content}\n"
                        if new_line != line:
                            line = new_line
                            modified = True
                    
                    new_lines.append(line)
                
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    files_fixed += 1
                    print(f"Fixed: {filepath}")

    print(f"\nTotal {files_fixed} files fixed.")

if __name__ == "__main__":
    fix_markdown_lists()