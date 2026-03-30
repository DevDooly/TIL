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
                    
                    if stripped.startswith("```"):
                        code_block_open = not code_block_open
                        continue
                    if code_block_open:
                        continue
                        
                    # 리스트 항목 발견
                    if list_pattern.match(line):
                        if i == 0: continue # 파일 첫 줄이 리스트면 통과
                        
                        prev_line = lines[i-1].strip()
                        # 이전 줄이 비어있지 않은 경우 체크
                        if prev_line:
                            # 이전 줄도 같은 레벨의 리스트면 통과
                            if list_pattern.match(lines[i-1]):
                                continue
                            # 이전 줄이 리스트가 아닌데 비어있지 않으면 무조건 에러 (헤더 포함)
                            # 마크다운 표준상 리스트 시작 전에는 빈 줄이 있어야 함
                            if not prev_line.startswith('<!--') and prev_line != '---':
                                print(f"❌ [Format Error] {filepath} (Line {i+1})")
                                print(f"   리스트 시작 전에 반드시 빈 줄이 필요합니다.")
                                print(f"   Prev: {prev_line}")
                                print(f"   Curr: {stripped}\n")
                                issues_found = True

                if code_block_open:
                    print(f"❌ [Syntax Error] {filepath}: 코드 블록이 닫히지 않았습니다.")
                    issues_found = True

    if issues_found:
        print("🚨 Markdown 에러가 발견되었습니다. 수정 후 다시 커밋해주세요.")
        exit(1)
    else:
        print("✅ 모든 Markdown 파일의 포맷이 올바릅니다.")
        exit(0)

if __name__ == "__main__":
    validate_markdown()