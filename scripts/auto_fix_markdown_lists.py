import os
import re

DOCS_DIR = "docs"

def fix_markdown_lists():
    # 리스트 패턴: - 또는 * 또는 숫자. 뒤에 공백 (내용 캡처)
    # 캡처: 1(인덴트), 2(마커), 3(내용)
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
                    
                    # 1. 코드 블록 상태 체크
                    if stripped.startswith("```"):
                        in_code_block = not in_code_block
                        new_lines.append(line)
                        continue
                    
                    if in_code_block:
                        new_lines.append(line)
                        continue
                    
                    # 2. 리스트 항목 감지
                    match = list_pattern.match(line)
                    if match:
                        indent = match.group(1)
                        marker = match.group(2)
                        content = match.group(3)
                        
                        # 리스트의 첫 시작인지 확인
                        if i > 0 and len(new_lines) > 0:
                            prev_line = new_lines[-1]
                            prev_stripped = prev_line.strip()
                            
                            # 이전 줄이 존재하고, 비어있지 않으며, 리스트 마커로 시작하지 않는 경우
                            # (즉, 헤더, 표, 구분선, 일반 문장 등 뒤에 바로 리스트가 붙은 경우)
                            if prev_stripped and not list_pattern.match(prev_line):
                                # 예외: HTML 주석은 개행 없이 붙여쓰는 경우가 많으므로 제외
                                if not prev_stripped.startswith('<!--'):
                                    new_lines.append("\n")
                                    modified = True
                        
                        # 3. 불렛 뒤 공백 표준화 (3개로 통일하여 가독성 및 렌더링 안정성 확보)
                        # (사용자가 1개를 원할 수도 있으나, 중첩 리스트 대응을 위해 3개가 권장되는 경우가 많음)
                        # 여기서는 사용자의 기존 의도(3개)를 존중하여 3개로 통일하거나, 
                        # 혹은 가장 안전한 1개로 통일. 
                        # 최근 문제들을 고려하여 '1개'로 엄격히 통일하되 개행을 확실히 함.
                        standardized_line = f"{indent}{marker}   {content}\n"
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
