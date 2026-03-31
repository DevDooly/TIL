import os
import re

DOCS_DIR = "docs"

def fix_markdown_lists():
    # 리스트 패턴: 시작부분에 - 또는 * 또는 숫자. 이 있고 그 뒤에 공백이 있는 경우
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
                    
                    # 코드 블록 상태 체크
                    if stripped.startswith("```"):
                        in_code_block = not in_code_block
                        new_lines.append(line)
                        continue
                    
                    if in_code_block:
                        new_lines.append(line)
                        continue
                    
                    match = list_pattern.match(line)
                    if match:
                        # 1. 이전 줄 체크 및 개행 강제화
                        if i > 0 and len(new_lines) > 0:
                            prev_line = new_lines[-1]
                            prev_stripped = prev_line.strip()
                            
                            # 이전 줄이 비어있지 않고, 리스트도 아니면 무조건 빈 줄 추가
                            # (헤더, 구분선, 일반 텍스트 모두 포함)
                            if prev_stripped and not list_pattern.match(prev_line):
                                # 단, 주석이나 구분선은 예외
                                if not prev_stripped.startswith('<!--') and prev_stripped != '---':
                                    new_lines.append("\n")
                                    modified = True
                        
                        # 2. 불렛 뒤 공백 1개로 표준화
                        indent = match.group(1)
                        marker = match.group(2)
                        content = match.group(3)
                        standardized_line = f"{indent}{marker} {content}\n"
                        if standardized_line != line:
                            line = standardized_line
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
