import os
import re

DOCS_DIR = "docs"

def fix_markdown_lists():
    # 리스트 패턴: 시작부분에 - 또는 * 또는 숫자. 이 있고 그 뒤에 하나 이상의 공백이 있는 경우
    # 캡처 그룹: 1(인덴트), 2(마커), 3(마커 뒤 공백들)
    list_pattern = re.compile(r'^(\s*)([-*]|\d+\.)(\s+)(.*)')
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
                    
                    # 코드 블록 진입/탈출 확인
                    if stripped_line.startswith("```"):
                        in_code_block = not in_code_block
                        new_lines.append(line)
                        continue
                        
                    if in_code_block:
                        new_lines.append(line)
                        continue
                        
                    match = list_pattern.match(line)
                    if match:
                        indent = match.group(1)
                        marker = match.group(2)
                        spacing = match.group(3)
                        content = match.group(4)
                        
                        # 1. 이전 줄 확인 및 개행 추가
                        if i > 0:
                            prev_line = lines[i-1].strip()
                            if prev_line and not list_pattern.match(prev_line) and not prev_line.startswith('#') and not prev_line.startswith('>'):
                                if not prev_line.startswith('<!--') and prev_line != '---':
                                    new_lines.append('\n')
                                    file_modified = True
                        
                        # 2. 공백 표준화 (* 뒤에 공백 1개로 통일)
                        # 단, 인덴트가 있는 서브리스트는 인덴트 유지
                        if spacing != ' ':
                            line = f"{indent}{marker} {content}\n"
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
