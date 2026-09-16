# Apache Avro: result 필드와 hashCode 지역 변수 충돌

Avro 스키마에 `result` 필드를 추가한 뒤 생성된 Java 코드가 컴파일되지 않는다면 `hashCode()`를 살펴볼 만하다. 필드와 지역 변수의 이름이 겹쳐 잘못된 변수를 참조하는 생성기 버그가 보고되어 있다.

## 이슈와 버전

`AVRO-4183`에 보고된 문제는 Avro **1.12.1**에서 발생하며, 수정 버전은 **1.12.2**로 표시되어 있다. `AVRO-4201`도 같은 문제의 중복 보고다. [AVRO-4183](https://issues.apache.org/jira/browse/AVRO-4183), [AVRO-4201](https://issues.apache.org/jira/browse/AVRO-4201)

## this.result는 명확한 필드 참조다

`result`는 Java 예약어가 아니므로 필드명으로 쓸 수 있다. 지역 변수와 이름이 같을 때 필드를 가리키려면 `this.result`처럼 구분하면 된다. 다음은 그 차이를 보여주는 최소 예제다.

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

생성된 파일에서 `this.`를 직접 붙이면 당장은 컴파일되지만 다음 빌드에서 덮어써진다. 생성기를 업데이트하거나 템플릿을 패치한 뒤 다시 생성해 확인해야 한다. 필드명을 바꾸는 방법은 스키마 호환성까지 검토해야 한다.

`python scripts/tests/test_java_examples.py`는 위 축약 코드의 컴파일 성공과 `this.` 제거 시 실패를 확인한다. Avro 생성기 전체를 실행하는 테스트와는 구분한다.
