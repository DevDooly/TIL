# Java: 연결된 GZIP 멤버 압축 해제

검증 기준: OpenJDK 21.0.9, 2026-09-07.

여러 GZIP 파일을 이어 붙이면 여러 멤버를 가진 GZIP 스트림이 된다. Java 21의 `GZIPInputStream`은 연결된 멤버를 읽을 수 있으므로, 멤버마다 스트림을 새로 생성하는 반복문은 필요하지 않다. 구현은 멤버의 trailer를 읽은 뒤 다음 header를 처리한다. [OpenJDK 21 구현](https://github.com/openjdk/jdk21u/blob/jdk-21.0.9-ga/src/java.base/share/classes/java/util/zip/GZIPInputStream.java), [GZIP 형식](https://www.rfc-editor.org/rfc/rfc1952.html)

## 스트리밍 예제

아래 코드를 `GzipStreams.java`로 저장한다. 전체 결과를 `byte[]`로 모으지 않고 출력 스트림에 전달하며, 압축 해제 후 크기 제한을 둔다.

```java
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Objects;
import java.util.zip.GZIPInputStream;

public final class GzipStreams {
    private GzipStreams() {}

    public static long decompress(
            InputStream source, OutputStream target, long maxOutputBytes)
            throws IOException {
        Objects.requireNonNull(source, "source");
        Objects.requireNonNull(target, "target");
        if (maxOutputBytes < 0) {
            throw new IllegalArgumentException("maxOutputBytes must be nonnegative");
        }

        long total = 0;
        // 유효한 인자로 호출하면 생성자 실패를 포함해 입력을 닫는다.
        try (InputStream ownedSource = source;
             GZIPInputStream gzip = new GZIPInputStream(ownedSource, 8192)) {
            byte[] buffer = new byte[8192];
            int read;
            while ((read = gzip.read(buffer)) != -1) {
                if (read > maxOutputBytes - total) {
                    throw new IOException("Decompressed output exceeds limit");
                }
                target.write(buffer, 0, read);
                total += read;
            }
        }
        // 출력의 flush/close는 호출자가 담당한다.
        return total;
    }
}
```

## 오류와 자원 소유권

- `EOFException`이나 `IOException`을 정상 종료로 바꾸지 않는다. CRC 오류나 잘린 데이터가 성공으로 처리될 수 있다.
- `GZIPInputStream.close()`는 감싼 입력도 닫는다. 같은 입력을 다음 멤버용 스트림에서 다시 사용하지 않는다.
- 실패 전에 일부 결과를 출력했을 수 있다. 파일을 원자적으로 교체하려면 임시 파일에 쓰고 검증 완료 후 목적 파일로 이동한다.
- 크기 제한과 별도로 네트워크 timeout과 작업 deadline을 설정한다.

## 형식 검증의 한계

Java 21 구현은 정상 멤버 뒤의 일부 잘못된 header/trailing bytes를 스트림 종료로 간주할 수 있다. 이 예제의 성공이 모든 입력 바이트의 엄격한 GZIP 형식을 보증하지는 않는다.

뒤에 붙은 비-GZIP 데이터도 오류로 처리해야 한다면 Apache Commons Compress의 `GzipCompressorInputStream`과 `setDecompressConcatenated(true)` 같은 명시적 정책을 검토한다. 버전을 고정하고 잘린 다음 header까지 테스트한다. [Commons Compress API](https://commons.apache.org/proper/commons-compress/apidocs/org/apache/commons/compress/compressors/gzip/GzipCompressorInputStream.html)

압축 바이트에서 `1f 8b`만 검색해 멤버 수를 세는 것도 안전하지 않다. 압축 본문에 같은 바이트가 나타날 수 있고 decoder의 read-ahead 때문에 하위 스트림 위치가 멤버 경계와 다를 수 있다.

## 회귀 검증

저장소 루트에서 `python scripts/tests/test_java_examples.py`를 실행하면 위 코드 블록을 추출해 JDK 21 이상으로 컴파일한다.

- 단일·다중 멤버, 중간의 빈 멤버
- CRC 손상과 잘린 trailer의 실패
- 압축 해제 크기 제한의 경계 및 초과
- 입력 닫힘과 출력 소유권, Java 21의 trailing bytes 허용 동작

실제 네트워크 스트림은 입력 구현과 timeout 조건을 추가로 검증한다.
