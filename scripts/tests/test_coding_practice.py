"""Compile the published solutions and compare with independent small-input oracles."""
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import unittest

from test_java_examples import java_tool

ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "docs/Language/Java/Java_Coding_Test_Practice.md"

HARNESS = r"""
import java.math.BigInteger;
import java.util.*;

public class PracticeChecks {
    static final Random RANDOM = new Random(20261014L);
    static void check(boolean condition) {
        if (!condition) throw new AssertionError("Practice result differs from oracle");
    }
    static long[] smallArray(int maximumLength, int bound) {
        long[] values = new long[RANDOM.nextInt(maximumLength + 1)];
        for (int i = 0; i < values.length; i++) values[i] = RANDOM.nextInt(bound);
        return values;
    }
    static void total() {
        check(Exercise01.total(new long[0]) == 0);
        long[] large = new long[100000];
        Arrays.fill(large, 1000000000000L);
        check(Exercise01.total(large) == 100000000000000000L);
        for (int t = 0; t < 300; t++) {
            long[] values = smallArray(40, 201);
            BigInteger expected = BigInteger.ZERO;
            for (int i = 0; i < values.length; i++) {
                values[i] = (values[i] - 100) * 1000000000L;
                expected = expected.add(BigInteger.valueOf(values[i]));
            }
            check(Exercise01.total(values) == expected.longValueExact());
        }
    }
    static String letters() {
        StringBuilder value = new StringBuilder();
        int size = RANDOM.nextInt(20);
        for (int i = 0; i < size; i++) value.append((char) ('a' + RANDOM.nextInt(26)));
        return value.toString();
    }
    static void commonCharacter() {
        check(!Exercise02.hasCommonCharacter("", "a"));
        check(!Exercise02.hasCommonCharacter("", ""));
        check(Exercise02.hasCommonCharacter("z", "z"));
        for (int t = 0; t < 500; t++) {
            String first = letters(), second = letters();
            boolean expected = false;
            for (int i = 0; i < first.length(); i++) {
                for (int j = 0; j < second.length(); j++) {
                    if (first.charAt(i) == second.charAt(j)) expected = true;
                }
            }
            check(Exercise02.hasCommonCharacter(first, second) == expected);
        }
    }
    static boolean reducedBrackets(String value) {
        while (true) {
            String next = value.replace("()", "").replace("[]", "").replace("{}", "");
            if (next.equals(value)) return next.isEmpty();
            value = next;
        }
    }
    static void brackets() {
        String[] fixed = {"", "(", ")", "([)]", "[(){}]", "{}[]()", "(()", "][]"};
        for (String value : fixed) check(Exercise03.isBalanced(value) == reducedBrackets(value));
        char[] alphabet = {'(', ')', '[', ']', '{', '}'};
        for (int t = 0; t < 800; t++) {
            StringBuilder value = new StringBuilder();
            int size = RANDOM.nextInt(25);
            for (int i = 0; i < size; i++) value.append(alphabet[RANDOM.nextInt(6)]);
            String input = value.toString();
            check(Exercise03.isBalanced(input) == reducedBrackets(input));
        }
        char[] deep = new char[200000];
        Arrays.fill(deep, 0, 100000, '(');
        Arrays.fill(deep, 100000, 200000, ')');
        check(Exercise03.isBalanced(new String(deep)));
    }
    static List<Integer> slowQueries(int[][] queries) {
        Map<Integer, Integer> counts = new HashMap<Integer, Integer>();
        List<Integer> answers = new ArrayList<Integer>();
        for (int[] query : queries) {
            int type = query[0], value = query[1];
            int old = counts.containsKey(value) ? counts.get(value) : 0;
            if (type == 1) counts.put(value, old + 1);
            else if (type == 2 && old > 0) counts.put(value, old - 1);
            else if (type == 3) {
                boolean found = false;
                for (int count : counts.values()) if (count == value) found = true;
                answers.add(found ? 1 : 0);
            }
        }
        return answers;
    }
    static void queries() {
        int[][] fixed = {{2, 99}, {3, 1}, {1, 5}, {1, 5}, {1, 6}, {1, 6},
            {3, 2}, {2, 5}, {3, 2}, {2, 6}, {3, 2}, {2, 5}, {2, 5}, {3, 1}};
        check(Exercise04.processQueries(fixed).equals(slowQueries(fixed)));
        check(Exercise04.processQueries(new int[0][2]).isEmpty());
        for (int t = 0; t < 250; t++) {
            int[][] input = new int[1 + RANDOM.nextInt(100)][2];
            for (int[] query : input) {
                query[0] = 1 + RANDOM.nextInt(3);
                query[1] = 1 + RANDOM.nextInt(query[0] == 3 ? 12 : 8);
            }
            check(Exercise04.processQueries(input).equals(slowQueries(input)));
        }
    }
    static int exhaustiveItems(long[] prices, long budget) {
        int best = 0;
        for (int mask = 0; mask < (1 << prices.length); mask++) {
            long cost = 0;
            for (int i = 0; i < prices.length; i++) if ((mask & (1 << i)) != 0) cost += prices[i];
            if (cost <= budget) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }
    static void items() {
        check(Exercise05.maxItems(new long[0], 0) == 0);
        check(Exercise05.maxItems(new long[] {1000000000000L, 1000000000000L}, 2000000000000L) == 2);
        for (int t = 0; t < 250; t++) {
            long[] input = smallArray(11, 25);
            for (int i = 0; i < input.length; i++) input[i]++;
            long[] before = input.clone();
            long budget = RANDOM.nextInt(100);
            check(Exercise05.maxItems(input, budget) == exhaustiveItems(input, budget));
            check(Arrays.equals(input, before));
        }
    }
    static void pairs() {
        check(Exercise06.countPairs(new long[] {0, 1000000000000L}, 1000000000000L) == 1);
        for (int t = 0; t < 400; t++) {
            Set<Long> unique = new HashSet<Long>();
            int size = RANDOM.nextInt(35);
            while (unique.size() < size) unique.add((long) RANDOM.nextInt(100));
            long[] input = new long[size];
            int index = 0;
            for (long value : unique) input[index++] = value;
            for (int i = input.length - 1; i > 0; i--) {
                int j = RANDOM.nextInt(i + 1);
                long tmp = input[i]; input[i] = input[j]; input[j] = tmp;
            }
            long[] before = input.clone();
            long k = 1 + RANDOM.nextInt(110), expected = 0;
            for (int i = 0; i < size; i++) for (int j = i + 1; j < size; j++) {
                if (Math.abs(input[i] - input[j]) == k) expected++;
            }
            check(Exercise06.countPairs(input, k) == expected);
            check(Arrays.equals(input, before));
        }
    }
    static int[] floyd(int n, int[][] edges, int start) {
        int[][] distance = new int[n + 1][n + 1];
        for (int i = 1; i <= n; i++) {
            Arrays.fill(distance[i], 1000000); distance[i][i] = 0;
        }
        for (int[] edge : edges) if (edge[0] != edge[1]) {
            distance[edge[0]][edge[1]] = distance[edge[1]][edge[0]] = 1;
        }
        for (int k = 1; k <= n; k++) for (int i = 1; i <= n; i++) for (int j = 1; j <= n; j++) {
            distance[i][j] = Math.min(distance[i][j], distance[i][k] + distance[k][j]);
        }
        int[] result = new int[n + 1]; result[0] = -1;
        for (int i = 1; i <= n; i++) result[i] = distance[start][i] >= 1000000 ? -1 : distance[start][i];
        return result;
    }
    static void graph() {
        check(Arrays.equals(Exercise07.distances(1, new int[0][2], 1), new int[] {-1, 0}));
        for (int t = 0; t < 200; t++) {
            int n = 1 + RANDOM.nextInt(9), m = RANDOM.nextInt(25), start = 1 + RANDOM.nextInt(n);
            int[][] edges = new int[m][2];
            for (int[] edge : edges) {
                edge[0] = 1 + RANDOM.nextInt(n); edge[1] = 1 + RANDOM.nextInt(n);
            }
            check(Arrays.equals(Exercise07.distances(n, edges, start), floyd(n, edges, start)));
        }
    }
    static long slowWindows(long[] values, int width, long target) {
        long answer = 0;
        for (int left = 0; left + width <= values.length; left++) {
            long sum = 0;
            for (int i = left; i < left + width; i++) sum += values[i];
            if (sum == target) answer++;
        }
        return answer;
    }
    static void windows() {
        check(Exercise08.countWindows(new long[] {1000000000L, 1000000000L, 1000000000L}, 3, 3000000000L) == 1);
        for (int t = 0; t < 400; t++) {
            long[] values = smallArray(35, 21);
            for (int i = 0; i < values.length; i++) values[i] -= 10;
            int width = 1 + RANDOM.nextInt(40);
            long target = RANDOM.nextInt(101) - 50;
            check(Exercise08.countWindows(values, width, target) == slowWindows(values, width, target));
        }
    }
    static int slowMerges(long[] values, long threshold) {
        List<BigInteger> items = new ArrayList<BigInteger>();
        for (long value : values) items.add(BigInteger.valueOf(value));
        BigInteger target = BigInteger.valueOf(threshold);
        int count = 0;
        while (!items.isEmpty()) {
            Collections.sort(items);
            if (items.get(0).compareTo(target) >= 0) return count;
            if (items.size() < 2) return -1;
            BigInteger first = items.remove(0), second = items.remove(0);
            items.add(first.add(second.multiply(BigInteger.valueOf(2)))); count++;
        }
        return 0;
    }
    static void merges() {
        long[][] fixed = {new long[0], {0}, {0, 0}, {999999999L, 999999999L, 999999999L}, {0, 1000000000L}};
        for (long[] values : fixed) {
            check(Exercise09.minimumMerges(values, 1000000000L) == slowMerges(values, 1000000000L));
            check(Exercise09.minimumMerges(values, 0) == 0);
        }
        for (int t = 0; t < 350; t++) {
            long[] values = smallArray(20, 31), before = values.clone();
            long threshold = RANDOM.nextInt(80);
            check(Exercise09.minimumMerges(values, threshold) == slowMerges(values, threshold));
            check(Arrays.equals(values, before));
        }
    }
    public static void main(String[] args) {
        if ("01".equals(args[0])) total();
        else if ("02".equals(args[0])) commonCharacter();
        else if ("03".equals(args[0])) brackets();
        else if ("04".equals(args[0])) queries();
        else if ("05".equals(args[0])) items();
        else if ("06".equals(args[0])) pairs();
        else if ("07".equals(args[0])) graph();
        else if ("08".equals(args[0])) windows();
        else if ("09".equals(args[0])) merges();
        else throw new IllegalArgumentException(args[0]);
    }
}
"""


class CodingPracticeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="til-coding-practice-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.directory = Path(cls.tmp.name)
        cls.java = java_tool("java")
        text = DOCUMENT.read_text(encoding="utf-8")
        blocks = re.findall(r"^[ \t]*```java\s*\n(.*?)^[ \t]*```", text, re.MULTILINE | re.DOTALL)
        names = set()
        for block in blocks:
            source = textwrap.dedent(block)
            match = re.search(r"public (?:final )?class (Exercise\d{2})\b", source)
            if match:
                name = match.group(1)
                if name in names:
                    raise AssertionError(f"Duplicate exercise class: {name}")
                names.add(name)
                (cls.directory / f"{name}.java").write_text(source, encoding="utf-8")
        if names != {f"Exercise{i:02d}" for i in range(1, 10)}:
            raise AssertionError(f"Expected nine complete published solutions, found {names}")
        (cls.directory / "PracticeChecks.java").write_text(HARNESS, encoding="utf-8")
        result = subprocess.run(
            [java_tool("javac"), "--release", "8", "-encoding", "UTF-8",
             *[str(path) for path in cls.directory.glob("*.java")]],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    def run_check(self, case):
        result = subprocess.run(
            [self.java, "-cp", str(self.directory), "PracticeChecks", case],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_long_sum(self): self.run_check("01")
    def test_common_character(self): self.run_check("02")
    def test_balanced_brackets(self): self.run_check("03")
    def test_frequency_queries(self): self.run_check("04")
    def test_budget_subset_oracle(self): self.run_check("05")
    def test_difference_pairs(self): self.run_check("06")
    def test_bfs_against_floyd(self): self.run_check("07")
    def test_fixed_window_sums(self): self.run_check("08")
    def test_heap_merges_against_big_integer(self): self.run_check("09")

    def test_published_main_examples(self):
        expected = {
            "01": "3500000000\n0\n", "02": "true\nfalse\n", "03": "true\nfalse\n",
            "04": "[1, 0, 1]\n[0, 0]\n", "05": "3\n0\n", "06": "3\n1\n",
            "07": "[-1, 0, 1, 2, 1, 2, -1, -1]\n[-1, -1, 0, 1, -1]\n",
            "08": "2\n0\n", "09": "2\n-1\n",
        }
        for number, output in expected.items():
            with self.subTest(exercise=number):
                result = subprocess.run(
                    [self.java, "-cp", str(self.directory), "Exercise" + number],
                    capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.replace("\r\n", "\n"), output)


if __name__ == "__main__":
    unittest.main()
