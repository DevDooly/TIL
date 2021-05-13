# Tokenizer

토큰화는 단어 세기, 구문 분석, 맞춤법 검사, 말뭉치 생성 및 텍스트 통계 분석과 같은 많은 자연어 처리 작업에서 필요한 첫 번째 단계입니다.  
Tokenizer는 입력 텍스트를 토큰 스트림으로 변환합니다.  
여기서 각 토큰은 별도의 단어, 문장 부호, 숫자 / 금액, 날짜, 이메일, URL / URI 등입니다.  
또한, 문장 중간의 약어 및 날짜 케이스를 고려하여 토큰 스트림을 문장으로 나눕니다.

## Deep vs shallow tokenization

Shallow Tokenization(얕은 토큰화) 은 단순히 문장을 문자열(또는 출력 파일의 텍스트 라인)로 반환하며, 개별 토큰은 공백으로 구분됩니다.  
Deep Tokenization(깊은 토큰화) 는 토큰 유형 및 토큰에서 추출된 추가 정보(ex. 시간 => (년,월,일) 튜플) 로 토큰 개체를 반환합니다.  

기본적으로 명령 줄 도구는 얕은 토큰 화를 수행합니다. 명령 줄 도구로 심층적 인 토큰 화를 원하는 경우 --json 또는 --csv 스위치를 사용해야 합니다.

## Command Line
```
$ tokenize input.txt output.txt
```


## References
* https://pypi.org/project/tokenizer/
