import os
import re

DOCS_DIR = "docs"

def fix_markdown_lists():
    # 리스트 패턴: - 또는 * 또는 숫자. 뒤에 공백 (내용 캡처)
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
                    
                    # 1. 코드 블록 무시
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
                        # 리스트의 첫 시작인지 확인
                        if i > 0 and len(new_lines) > 0:
                            prev_line = new_lines[-1]
                            prev_stripped = prev_line.strip()
                            
                            # 이전 줄이 리스트 마커가 아니고, 비어있지도 않다면 무조건 개행 추가
                            # (헤더, 표, 구분선, 콜론으로 끝나는 문장 등 모든 텍스트 포함)
                            if prev_stripped and not list_pattern.match(prev_line):
                                # 예외: HTML 주석만 허용
                                if not prev_stripped.startswith('<!--'):
                                    new_lines.append("\n")
                                    modified = True
                        
                        # 3. 불렛 뒤 공백 표준화 (가장 안전한 1개로 통일)
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