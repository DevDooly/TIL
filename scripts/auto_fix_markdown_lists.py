import os
import re

DOCS_DIR = "docs"

def fix_markdown_lists():
    list_pattern = re.compile(r'^(\s*)([-*]|\d+\.)\s+')
    files_fixed = 0
    
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                new_lines = []
                in_code_block = False
                file_modified = False
                
                for i in range(len(lines)):
                    line = lines[i]
                    stripped_line = line.strip()
                    
                    if stripped_line.startswith("```"):
                        in_code_block = not in_code_block
                        new_lines.append(line)
                        continue
                        
                    if in_code_block:
                        new_lines.append(line)
                        continue
                        
                    # 1번째 줄 이후부터 검사
                    if i > 0 and list_pattern.match(stripped_line):
                        prev_line = lines[i-1].strip()
                        # 이전 줄이 비어있지 않고, 리스트도 아니고, 헤더도 아니고, 인용구도 아니면 빈 줄 추가
                        if prev_line and not list_pattern.match(prev_line) and not prev_line.startswith('#') and not prev_line.startswith('>'):
                            if not prev_line.startswith('<!--') and prev_line != '---':
                                new_lines.append('\n')
                                file_modified = True
                    
                    new_lines.append(line)
                
                if file_modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    files_fixed += 1
                    print(f"Fixed: {filepath}")

    print(f"\nTotal {files_fixed} files fixed.")

if __name__ == "__main__":
    fix_markdown_lists()
