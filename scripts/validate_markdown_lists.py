import os
import re

DOCS_DIR = "docs"

def validate_markdown_lists():
    issues_found = False
    
    # 정규식: 리스트 시작 패턴 (- , * , 1.  등)
    list_pattern = re.compile(r'^(\s*)([-*]|\d+\.)\s+')
    
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                in_code_block = False
                
                for i in range(1, len(lines)):
                    line = lines[i].strip()
                    prev_line = lines[i-1].strip()
                    
                    # 코드 블록 내부 무시
                    if line.startswith("```"):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        continue
                        
                    # 현재 줄이 리스트 항목인지 확인
                    if list_pattern.match(line):
                        # 이전 줄이 비어있지 않고, 이전 줄도 리스트가 아니고, 헤더(#)도 아니고, 인용구(>)도 아니면 경고
                        if prev_line and not list_pattern.match(prev_line) and not prev_line.startswith('#') and not prev_line.startswith('>'):
                            # HTML 주석이나 특정 마크다운 구분선은 예외 처리
                            if prev_line.startswith('<!--') or prev_line == '---':
                                continue
                            
                            print(f"❌ [Format Error] {filepath} (Line {i+1})")
                            print(f"   개행 누락: 리스트 시작 전에 빈 줄이 필요합니다.")
                            print(f"   Prev: {prev_line}")
                            print(f"   Curr: {line}\n")
                            issues_found = True

    if issues_found:
        print("🚨 Markdown 리스트 포맷 에러가 발견되었습니다. 수정 후 다시 커밋해주세요.")
        exit(1)
    else:
        print("✅ 모든 Markdown 파일의 리스트 포맷이 올바릅니다.")
        exit(0)

if __name__ == "__main__":
    validate_markdown_lists()
