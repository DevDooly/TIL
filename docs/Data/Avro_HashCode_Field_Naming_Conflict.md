# Apache Avro: result 필드와 hashCode 지역 변수 충돌

공식 이슈 확인: 2026-09-07. 공개된 생성기 버그와 진단 방법을 정리하며, 개별 프로젝트의 적용 버전과 재현 로그는 별도로 기록한다.

## 이슈와 버전

`AVRO-4183`은 Avro **1.12.1**의 생성된 `hashCode()`에서 지역 변수 `result`가 같은 이름의 필드를 가리는 문제다. 수정 버전은 **1.12.2**로 표기되어 있다. `AVRO-4201`은 중복 보고다. 기존 문서의 `AVRO-3831`, “1.11.2 발생 / 1.11.3 해결” 안내는 이 이슈의 근거와 맞지 않는다. [AVRO-4183](https://issues.apache.org/jira/browse/AVRO-4183), [AVRO-4201](https://issues.apache.org/jira/browse/AVRO-4201)

## this.result는 명확한 필드 참조다

핵심은 이름 자체가 아니라 **생성된 필드 참조에 `this.`가 빠졌는지**다. `result`는 Java 예약어가 아니다. 아래 축약 코드는 정상 컴파일된다.

```java
public final class AvroShadowing {
    private String result;

    @Override
    public int hashCode() {
        int result = 1;
        result = 31 * result + (this.result == null ? 0 : this.result.hashCode());
        return result;
    }
}
```

위 식의 `this.result`를 `result`로 바꾸면 지역 변수 `int result`를 참조한다. `int`를 `null`과 비교하거나 `hashCode()`를 호출하므로 컴파일 오류가 발생한다. 필드 타입과 생성 옵션에 따라 증상이 달라질 수 있으므로 실제 생성 파일을 확인한다. [Java 이름 가림 규칙](https://docs.oracle.com/javase/specs/jls/se21/html/jls-6.html#jls-6.4.1)

## 수정과 검증

1. runtime 외에 `avro-maven-plugin`, `avro-tools` 또는 Gradle 플러그인의 **생성기 버전**을 확인한다.
2. `result` 필드가 있는 최소 스키마와 기존 생성 옵션으로 코드를 생성하고 컴파일 실패를 재현한다.
3. 수정이 포함된 생성기로 올린 뒤 기존 생성물을 정리하고 다시 생성·컴파일한다.
4. 직렬화 왕복, reader/writer 스키마 호환성, `equals/hashCode` 일관성을 확인한다.

생성 파일의 수동 편집은 다음 빌드에서 사라진다. 템플릿을 패치한다면 재생성 테스트를 남긴다. 필드명 변경은 스키마 호환성에 영향을 줄 수 있으므로 단순 리팩토링으로 취급하지 않는다.

`python scripts/tests/test_java_examples.py`는 위 축약 코드의 컴파일 성공과 `this.` 제거 시 실패를 확인한다. Avro 생성기 전체를 실행하는 테스트와는 구분한다.
