import os
import re

DOCS_DIR = "docs"

def validate_markdown():
    issues_found = False
    
    # 정규식: 리스트 시작 패턴 (- , * , 1.  등)
    list_pattern = re.compile(r'^(\s*)([-*]|\d+\.)\s+')
    
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                code_block_open = False
                code_block_line = 0
                
                for i in range(len(lines)):
                    line = lines[i]
                    stripped = line.strip()
                    
                    # 1. 코드 블록 짝 맞춤 검사 (```)
                    if stripped.startswith("```"):
                        code_block_open = not code_block_open
                        code_block_line = i + 1
                        continue
                    
                    if code_block_open:
                        continue
                        
                    # 2. 리스트 개행 검사 (코드 블록 밖에서만)
                    if i > 0 and list_pattern.match(stripped):
                        prev_line = lines[i-1].strip()
                        # 이전 줄이 비어있지 않고, 리스트/헤더/인용구/주석/구분선이 아니면 에러
                        if prev_line and not list_pattern.match(prev_line) and \
                           not prev_line.startswith('#') and not prev_line.startswith('>') and \
                           not prev_line.startswith('<!--') and prev_line != '---':
                            
                            print(f"❌ [Format Error] {filepath} (Line {i+1})")
                            print(f"   개행 누락: 리스트 시작 전에 빈 줄이 필요합니다.")
                            print(f"   Prev: {prev_line}")
                            print(f"   Curr: {stripped}\n")
                            issues_found = True
                
                # 파일 끝났는데 코드 블록이 열려 있는 경우
                if code_block_open:
                    print(f"❌ [Syntax Error] {filepath} (Line {code_block_line})")
                    print(f"   코드 블록(```)이 닫히지 않았습니다.\n")
                    issues_found = True

    if issues_found:
        print("🚨 Markdown 에러가 발견되었습니다. 수정 후 다시 커밋해주세요.")
        exit(1)
    else:
        print("✅ 모든 Markdown 파일의 포맷이 올바릅니다.")
        exit(0)

if __name__ == "__main__":
    validate_markdown()
