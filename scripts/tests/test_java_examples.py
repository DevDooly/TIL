"""Compile the actual Java fences and exercise regressions; requires JDK 21+."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def java_tool(name):
    home = os.environ.get("JAVA_HOME")
    if home:
        candidate = Path(home) / "bin" / (name + (".exe" if os.name == "nt" else ""))
        if candidate.is_file():
            return str(candidate)
    found = shutil.which(name)
    if not found:
        raise RuntimeError(f"{name} is required (JDK 21+)")
    return found


def extract_java(path, class_name):
    text = (ROOT / path).read_text(encoding="utf-8")
    for block in re.findall(r"```java\n(.*?)```", text, re.DOTALL):
        if f"class {class_name} " in block:
            return block
    raise AssertionError(f"Java class {class_name} missing from {path}")


HARNESS = r"""
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.concurrent.*;
import java.util.zip.GZIPOutputStream;

public final class ExampleChecks {
    static void check(boolean ok) {
        if (!ok) throw new AssertionError();
    }

    interface CheckedAction { void run() throws Exception; }

    static void expectIo(CheckedAction action) throws Exception {
        try { action.run(); }
        catch (IOException expected) { return; }
        throw new AssertionError("Expected IOException");
    }

    static byte[] gzip(String s) throws IOException {
        var out = new ByteArrayOutputStream();
        try (var gz = new GZIPOutputStream(out)) {
            gz.write(s.getBytes(StandardCharsets.UTF_8));
        }
        return out.toByteArray();
    }

    static byte[] concat(byte[]... parts) throws IOException {
        var out = new ByteArrayOutputStream();
        for (byte[] part : parts) out.write(part);
        return out.toByteArray();
    }

    static String decode(byte[] data, long limit) throws IOException {
        var out = new ByteArrayOutputStream();
        long count = GzipStreams.decompress(new ByteArrayInputStream(data), out, limit);
        check(count == out.size());
        return out.toString(StandardCharsets.UTF_8);
    }

    static class TrackedInput extends ByteArrayInputStream {
        boolean closed;
        TrackedInput(byte[] data) { super(data); }
        @Override public void close() { closed = true; }
    }

    static class TrackedOutput extends ByteArrayOutputStream {
        boolean closed;
        @Override public void close() { closed = true; }
    }

    public static void main(String[] args) throws Exception {
        switch (args[0]) {
            case "single" -> check(decode(gzip("hello"), 5).equals("hello"));
            case "members" -> {
                var data = concat(gzip("hello"), gzip(""), gzip("\uD55C\uAE00"));
                check(decode(data, 100).equals("hello\uD55C\uAE00"));
                check(decode(gzip(""), 0).isEmpty());
            }
            case "crc" -> {
                byte[] bad = gzip("hello");
                bad[bad.length - 8] ^= 1;
                expectIo(() -> decode(bad, 100));
                expectIo(() -> decode(concat(gzip("good"), bad), 100));
            }
            case "truncated" -> {
                byte[] data = gzip("hello");
                expectIo(() -> decode(Arrays.copyOf(data, data.length - 3), 100));
            }
            case "limit" -> {
                expectIo(() -> decode(gzip("hello"), 4));
                expectIo(() -> decode(concat(gzip("abc"), gzip("def")), 5));
            }
            case "ownership" -> {
                var input = new TrackedInput(gzip("hello"));
                var output = new TrackedOutput();
                GzipStreams.decompress(input, output, 5);
                check(input.closed && !output.closed);
                var invalid = new TrackedInput(new byte[] {1, 2, 3});
                expectIo(() -> GzipStreams.decompress(invalid, output, 10));
                check(invalid.closed && !output.closed);
            }
            case "trailing" -> {
                // Documents this JDK decoder's permissive trailing-data behavior.
                check(decode(concat(gzip("ok"), new byte[] {1, 2, 3}), 2).equals("ok"));
            }
            case "bounded" -> {
                var executor = BoundedDbExecutor.create(1, 1);
                var started = new CountDownLatch(1);
                var release = new CountDownLatch(1);
                try {
                    var first = executor.submit(() -> {
                        check(!Thread.currentThread().isVirtual());
                        started.countDown();
                        release.await();
                        return 1;
                    });
                    check(started.await(5, TimeUnit.SECONDS));
                    var second = executor.submit(() -> 2);
                    boolean rejected = false;
                    try { executor.submit(() -> 3); }
                    catch (RejectedExecutionException expected) { rejected = true; }
                    check(rejected);
                    release.countDown();
                    check(first.get(5, TimeUnit.SECONDS) == 1);
                    check(second.get(5, TimeUnit.SECONDS) == 2);
                } finally {
                    release.countDown();
                    executor.shutdownNow();
                    check(executor.awaitTermination(5, TimeUnit.SECONDS));
                }
            }
            default -> throw new IllegalArgumentException(args[0]);
        }
    }
}
"""


class JavaExamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="til-java-test-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.directory = Path(cls.tmp.name)
        cls.javac = java_tool("javac")
        cls.java = java_tool("java")
        cases = {
            "GzipStreams": "docs/Language/Java/Concatenated_Gzip_Decompression.md",
            "AvroShadowing": "docs/Troubleshooting/Avro_HashCode_Field_Naming_Conflict.md",
            "BoundedDbExecutor": "docs/Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md",
        }
        for name, doc in cases.items():
            (cls.directory / f"{name}.java").write_text(
                extract_java(doc, name), encoding="utf-8")
        (cls.directory / "ExampleChecks.java").write_text(HARNESS, encoding="utf-8")
        result = subprocess.run(
            [cls.javac, "--release", "21", "-encoding", "UTF-8",
             *[str(p) for p in cls.directory.glob("*.java")]],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    def run_check(self, case):
        result = subprocess.run(
            [self.java, "-cp", str(self.directory), "ExampleChecks", case],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_single_member(self): self.run_check("single")
    def test_multiple_and_empty_members(self): self.run_check("members")
    def test_corrupt_crc(self): self.run_check("crc")
    def test_truncated_trailer(self): self.run_check("truncated")
    def test_output_limit(self): self.run_check("limit")
    def test_stream_ownership(self): self.run_check("ownership")
    def test_trailing_bytes_behavior(self): self.run_check("trailing")
    def test_saturated_executor_rejects(self): self.run_check("bounded")

    def test_unqualified_avro_field_fails_compilation(self):
        source = (self.directory / "AvroShadowing.java").read_text(encoding="utf-8")
        broken = source.replace("AvroShadowing", "AvroShadowingBroken").replace(
            "this.result", "result")
        path = self.directory / "AvroShadowingBroken.java"
        path.write_text(broken, encoding="utf-8")
        result = subprocess.run(
            [self.javac, "-J-Duser.language=en", "--release", "21", str(path)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("int cannot be dereferenced", result.stderr)


if __name__ == "__main__":
    unittest.main()
