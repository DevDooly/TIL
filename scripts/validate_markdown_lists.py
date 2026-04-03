import os
import re

DOCS_DIR = "docs"

def validate_markdown():
    issues_found = False
    # 리스트 패턴: - 또는 * 또는 숫자. 뒤에 공백
    list_pattern = re.compile(r'^(\s*)([-*]|\d+\.)\s+')
    
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                code_block_open = False
                for i in range(len(lines)):
                    line = lines[i]
                    stripped = line.strip()
                    
                    # 1. 코드 블록 상태 체크
                    if stripped.startswith("```"):
                        code_block_open = not code_block_open
                        continue
                    if code_block_open:
                        continue
                        
                    # 2. 리스트 항목 발견
                    if list_pattern.match(line):
                        if i == 0: continue
                        
                        prev_line = lines[i-1].strip()
                        # 이전 줄이 비어있지 않고, 리스트 마커도 없는 경우 (순수 텍스트, 헤더, 표, 구분선 등)
                        if prev_line and not list_pattern.match(lines[i-1]):
                            # 예외: HTML 주석
                            if not prev_line.startswith('<!--'):
                                print(f"❌ [Format Error] {filepath} (Line {i+1})")
                                print(f"   리스트 시작 전에 반드시 빈 줄이 필요합니다.")
                                print(f"   Prev: {prev_line}")
                                print(f"   Curr: {stripped}\n")
                                issues_found = True
                        
                        # 3. 추가 검증: 불렛 뒤 공백이 3개인지 확인 (가독성 표준)
                        # (필수는 아니지만 프로젝트의 일관성을 위해 체크)
                        # if not re.match(r'^(\s*)([-*]|\d+\.)   ', line):
                        #     pass 

                if code_block_open:
                    print(f"❌ [Syntax Error] {filepath}: 코드 블록이 닫히지 않았습니다.")
                    issues_found = True

    if issues_found:
        print("🚨 Markdown 에러가 발견되었습니다. scripts/auto_fix_markdown_lists.py 를 실행하세요.")
        exit(1)
    else:
        print("✅ 모든 Markdown 파일의 포맷이 올바릅니다.")
        exit(0)

if __name__ == "__main__":
    validate_markdown()
