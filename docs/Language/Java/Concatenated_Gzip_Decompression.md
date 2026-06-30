# Java: Concatenated GZIP 스트림 압축 해제 (Unzip)

Java의 표준 `GZIPInputStream`은 일반적으로 단일 GZIP 멤버(member)만을 압축 해제합니다. 하지만 여러 개의 GZIP 파일이 단순히 연결(concatenate)되어 하나의 파일로 합쳐진 "Concatenated GZIP" 스트림의 경우, 모든 GZIP 멤버를 순차적으로 압축 해제해야 합니다. 이는 주로 로그 파일이나 아카이브 파일에서 발생할 수 있습니다.

본 문서에서는 `InputStream`으로부터 Concatenated GZIP 스트림을 받아 모든 GZIP 멤버를 압축 해제하는 Java 함수를 제공합니다.

---

## 1. Concatenated GZIP 이해

GZIP 형식은 RFC 1952에 정의되어 있으며, 여러 개의 GZIP 스트림을 단순히 연결하여 하나의 파일로 만들 수 있도록 설계되어 있습니다. 예를 들어, `cat file1.gz file2.gz > combined.gz`와 같이 파일을 합칠 수 있습니다.

Java의 `java.util.zip.GZIPInputStream`은 기본적으로 스트림에서 첫 번째 GZIP 멤버만을 읽고 압축을 해제합니다. 따라서 Concatenated GZIP 파일을 처리하려면, 첫 번째 멤버의 압축 해제가 완료된 후 스트림의 남은 부분에서 다음 GZIP 멤버를 찾아 압축 해제하는 과정을 반복해야 합니다.

---

## 2. Concatenated GZIP 압축 해제 함수

다음 `decompressConcatenatedGzip` 함수는 `InputStream`을 인자로 받아 모든 연결된 GZIP 멤버를 순차적으로 압축 해제하고, 압축 해제된 데이터를 `byte[]` 배열로 반환합니다.

```java
import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.EOFException;
import java.io.FileInputStream; // 예제 사용을 위함
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets; // 예제 사용을 위함
import java.util.zip.GZIPInputStream;

public class GzipUtils {

    /**
     * Concatenated GZIP 스트림에서 모든 GZIP 멤버를 압축 해제합니다.
     * 일반 GZIPInputStream은 단일 GZIP 멤버만 처리하지만, 이 함수는 연결된 모든 멤버를 순차적으로 처리합니다.
     *
     * @param compressedStream 압축된 Concatenated GZIP InputStream
     * @return 압축 해제된 모든 데이터의 byte 배열
     * @throws IOException 압축 해제 중 입출력 오류 또는 GZIP 형식 오류 발생 시
     */
    public static byte[] decompressConcatenatedGzip(InputStream compressedStream) throws IOException {
        ByteArrayOutputStream decompressedOutput = new ByteArrayOutputStream();
        // 성능 향상을 위해 InputStream을 버퍼링합니다.
        BufferedInputStream bufferedInput = new BufferedInputStream(compressedStream);

        while (true) {
            try (GZIPInputStream gzipInputStream = new GZIPInputStream(bufferedInput)) {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = gzipInputStream.read(buffer)) != -1) {
                    decompressedOutput.write(buffer, 0, bytesRead);
                }
                // 현재 GZIP 멤버의 압축 해제가 완료되면,
                // GZIPInputStream은 암묵적으로 내부 스트림을 닫지만,
                // 하위 스트림인 'bufferedInput'은 계속 열려 있으며 다음 GZIP 멤버의 시작 부분에 위치합니다.

            } catch (EOFException e) {
                // 스트림 끝에 도달했으나 GZIP 스트림이 불완전할 경우 발생할 수 있습니다.
                // 대부분의 경우, 더 이상 GZIP 멤버가 없다는 신호로 간주할 수 있습니다.
                break;
            } catch (IOException e) {
                // "Not in GZIP format" 등의 IOException이 발생하면,
                // 더 이상 GZIP 멤버가 없거나 (EOF 도달) 실제 GZIP 형식 오류일 수 있습니다.
                
                // underlying 스트림이 실제로 끝에 도달했는지 확인합니다.
                // bufferedInput.mark(1)은 최소 한 바이트를 읽기 위해 마크합니다.
                bufferedInput.mark(1); 
                int nextByte = bufferedInput.read();
                bufferedInput.reset(); // 마크된 위치로 스트림을 되돌립니다.
                
                if (nextByte == -1) { // underlying 스트림이 실제로 EOF에 도달했다면, 모든 GZIP 멤버 처리가 완료된 것입니다.
                    break; // 루프 종료
                } else {
                    // 여전히 데이터가 남아있지만 GZIPInputStream 생성이 실패했다면,
                    // 유효하지 않은 GZIP 형식으로 간주하고 에러를 던집니다.
                    throw e; 
                }
            }
        }
        return decompressedOutput.toByteArray();
    }

    /**
     * 주어진 InputStream이 Concatenated GZIP 형식인지 확인합니다.
     * 즉, 첫 번째 GZIP 멤버 이후에 또 다른 GZIP 멤버가 존재하는지 확인합니다.
     *
     * @param inputStream GZIP 압축이 예상되는 InputStream
     * @return 첫 번째 GZIP 멤버 이후에 또 다른 GZIP 멤버가 존재하면 true, 그렇지 않으면 false
     * @throws IOException 입출력 오류 발생 시
     */
    public static boolean isConcatenatedGzip(InputStream inputStream) throws IOException {
        // BufferedInputStream을 사용하여 mark/reset 기능을 활용합니다.
        // GZIPInputStream의 close()가 하위 스트림을 닫는 것을 방지하기 위해 NoCloseInputStream으로 래핑합니다.
        BufferedInputStream bufferedInput = new BufferedInputStream(inputStream);
        
        try (GZIPInputStream gzipInputStream = new GZIPInputStream(new NoCloseInputStream(bufferedInput))) {
            // 첫 번째 GZIP 멤버의 데이터를 모두 소비합니다.
            // (실제로 데이터를 읽을 필요는 없지만, 스트림 포인터를 끝까지 이동시킵니다.)
            byte[] buffer = new byte[4096];
            while (gzipInputStream.read(buffer) != -1) {
                // 데이터를 읽어 스트림 포인터를 이동시킵니다.
            }
            // gzipInputStream은 여기서 닫히지만, NoCloseInputStream 덕분에 bufferedInput은 열려 있습니다.

            // 첫 번째 GZIP 멤버가 끝난 후, 다음 바이트를 확인하여 GZIP 매직 넘버가 있는지 봅니다.
            // GZIP 매직 넘버는 0x1f 0x8b 입니다.
            bufferedInput.mark(2); // 다음 2바이트를 마크합니다.
            int id1 = bufferedInput.read();
            int id2 = bufferedInput.read();
            bufferedInput.reset(); // 읽은 2바이트를 다시 스트림으로 되돌립니다.

            // 스트림이 EOF가 아니고 (id1 != -1), 다음 2바이트가 GZIP 매직 넘버와 일치하면 Concatenated GZIP입니다.
            return id1 != -1 && id1 == (GZIPInputStream.GZIP_MAGIC & 0xFF) && id2 == ((GZIPInputStream.GZIP_MAGIC >>> 8) & 0xFF);

        } catch (IOException e) {
            // GZIPInputStream 생성자가 IOException을 던졌다는 것은
            // - 스트림이 아예 비어있거나
            // - 유효한 GZIP 형식이 아니거나
            // - 첫 번째 멤버가 끝나지 않았는데 스트림이 끝났다는 의미입니다.
            // 이 경우 Concatenated GZIP이 아니라고 판단할 수 있습니다.
            return false;
        }
    }

    /**
     * GZIPInputStream이 내부의 InputStream을 닫는 것을 방지하기 위한 헬퍼 클래스.
     */
    private static class NoCloseInputStream extends FilterInputStream {
        public NoCloseInputStream(InputStream in) {
            super(in);
        }

        @Override
        public void close() throws IOException {
            // 아무것도 하지 않아 하위 스트림을 닫지 않습니다.
        }
    }

    /**
     * 예제 사용법: 파일에서 Concatenated GZIP 압축 해제 및 Concatenated 여부 확인
     */
    public static void main(String[] args) {
        // 테스트용 GZIP 파일 생성 (실제 파일 경로로 변경 필요)
        // 1. 단일 GZIP 파일 생성:
        //    echo "Single Gzip Content" | gzip > single.gz
        // 2. Concatenated GZIP 파일 생성:
        //    echo "First part of the data" | gzip > part1.gz
        //    echo "Second part of the data" | gzip > part2.gz
        //    cat part1.gz part2.gz > combined.gz
        //    rm part1.gz part2.gz

        String singleGzipPath = "single.gz"; // 단일 GZIP 파일 경로
        String concatenatedGzipPath = "combined.gz"; // Concatenated GZIP 파일 경로

        System.out.println("--- Concatenated GZIP 압축 해제 테스트 ---");
        try (InputStream fileInputStream = new FileInputStream(concatenatedGzipPath)) {
            byte[] decompressedData = decompressConcatenatedGzip(fileInputStream);
            String result = new String(decompressedData, StandardCharsets.UTF_8);
            System.out.println(concatenatedGzipPath + " 압축 해제된 데이터:\n" + result);
        } catch (IOException e) {
            System.err.println(concatenatedGzipPath + " 압축 해제 중 에러: " + e.getMessage());
        }

        System.out.println("\n--- Concatenated GZIP 여부 확인 테스트 ---");
        try (InputStream singleGzipStream = new FileInputStream(singleGzipPath)) {
            System.out.println(singleGzipPath + "은 Concatenated GZIP인가? " + isConcatenatedGzip(singleGzipStream));
        } catch (IOException e) {
            System.err.println(singleGzipPath + " 확인 중 에러: " + e.getMessage());
        }

        try (InputStream concatenatedGzipStream = new FileInputStream(concatenatedGzipPath)) {
            System.out.println(concatenatedGzipPath + "은 Concatenated GZIP인가? " + isConcatenatedGzip(concatenatedGzipStream));
        } catch (IOException e) {
            System.err.println(concatenatedGzipPath + " 확인 중 에러: " + e.getMessage());
        }
    }
    }
}
```

---

## 3. 사용 예시

위 `GzipUtils` 클래스를 사용하여 Concatenated GZIP 파일을 압축 해제하는 방법은 다음과 같습니다.

1.  **Concatenated GZIP 파일 준비:**
    예를 들어, 터미널에서 다음 명령어를 사용하여 테스트 파일을 만들 수 있습니다.
    ```bash
    echo "First part of the data" | gzip > part1.gz
    echo "Second part of the data" | gzip > part2.gz
    cat part1.gz part2.gz > combined.gz
    rm part1.gz part2.gz
    ```
2.  **Java 코드에서 사용:**
    `GzipUtils.main` 메소드의 예시처럼 `FileInputStream`을 사용하여 `decompressConcatenatedGzip` 함수에 전달합니다.

```java
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) {
        String filePath = "combined.gz"; // 실제 Concatenated GZIP 파일 경로로 변경

        try (InputStream fileInputStream = new FileInputStream(filePath)) {
            byte[] decompressedData = GzipUtils.decompressConcatenatedGzip(fileInputStream);
            String result = new String(decompressedData, StandardCharsets.UTF_8);
            System.out.println("압축 해제된 데이터:
" + result);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

---

## 4. 고려 사항

*   **성능:** 대용량 파일 처리 시 `BufferedInputStream`을 사용하여 입출력 성능을 향상시키는 것이 좋습니다.
*   **메모리:** 압축 해제된 데이터 전체를 `ByteArrayOutputStream`에 저장하므로, 매우 큰 파일의 경우 OutOfMemoryError가 발생할 수 있습니다. 이 경우, 압축 해제된 데이터를 바로 다른 `OutputStream`으로 스트리밍하거나, `read()` 호출 시마다 처리하는 방식으로 변경해야 합니다.
*   **GZIP 형식 오류:** `GZIPInputStream` 생성자나 `read` 메소드에서 발생하는 `IOException`은 GZIP 형식 오류를 나타낼 수 있습니다. 예제 코드에서는 `bufferedInput.mark(1)`을 통해 스트림의 끝을 확인하여 단순한 EOF와 실제 형식 오류를 구분합니다.
