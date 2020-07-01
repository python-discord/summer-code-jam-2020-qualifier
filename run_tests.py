from __future__ import annotations

import collections
import datetime
import io
import math
import sys
import textwrap
import timeit
import traceback
import types
import typing
import unittest

TITLE = "Python Discord Summer Code Jam 2020: Qualifier Test Results"
CONSOLE_WIDTH = 100


class SkippedTest(Exception):
    """Indicates that a test method was skipped."""


class QualifierTestRunner:
    """Test runner for our code jam qualifier test suite."""

    def __init__(self) -> None:
        self.stream = StreamWrapper(sys.stderr, max_width=CONSOLE_WIDTH)

    def write_header(self) -> None:
        """Write a header for this test run."""
        self.stream.write_separator("=")
        self.stream.write(f"{TITLE}\n")
        self.stream.write_separator("=")
        self.stream.writeln(
            f"Date: {datetime.datetime.utcnow().strftime(r'%Y-%m-%d %H:%M:%S')} UTC"
        )

    def write_footer(self, result: QualifierTestResult, duration: float) -> None:
        """Write a footer for this test run."""
        self.stream.writeln()
        self.stream.write_separator("=")
        self.stream.writeln(f"Test Suite Summary")
        self.stream.write_separator("-")
        if hasattr(result, "results"):
            self.stream.write(
                f"{' '*50} PASSED   FAILED   TOTAL   RESULT"
                "\n"
            )
            for section, section_results in result.results.items():
                section = textwrap.shorten(section, width=50, placeholder="...")
                total = len(section_results)
                passed = sum(test_result for test_result in section_results.values())
                failed = total - passed
                result = "FAIL" if failed else "PASS"
                self.stream.write(
                    f"{section:<50}  {passed:^6}   {failed:^6}  {total:^5}    {result}\n"
                )

        self.stream.write_separator("=")
        self.stream.writeln(f"Total running time: {duration:.3f}s")

    def run(self, test: unittest.TestSuite) -> None:
        """Run a test suite containing `unittest.TestCase` tests."""
        result = QualifierTestResult(self.stream)
        self.write_header()

        # Record the start time
        start = timeit.default_timer()

        # Pass the TestResult instance to the test suite to run the tests
        test(result)

        # Record the end time
        duration = timeit.default_timer() - start

        self.write_footer(result, duration)


TestOutcome = typing.Tuple[typing.Type[BaseException], BaseException, types.TracebackType]
TestClass = collections.namedtuple("TestClass", "type name")


class StreamWrapper:
    """Wrap an `io.TextIOBase` derived stream with utility methods."""

    def __init__(self, stream: io.TextIOBase, max_width: int = 100, verbosity: int = 0) -> None:
        self.stream = stream
        self.max_width = max_width
        self.verbosity = verbosity

    def __getattr__(self, attr: str) -> typing.Any:
        """Delegate attributes to the `io.TextIOBase` derived stream object."""
        return getattr(self.stream, attr)

    @staticmethod
    def fixed_width_text(text: str, width: int) -> str:
        """Create a string with a certain width by truncating and/or right-padding `text`."""
        return f"{text[:width]:<{width}}"

    def writeln(self, text: str = "") -> None:
        """Write a line to the stream."""
        if text:
            self.stream.write(text[:self.max_width])
        self.stream.write("\n")

    def write_separator(self, char: str = "-", length: typing.Optional[int] = None) -> None:
        """Write a separator line to the stream."""
        if not length:
            length = self.max_width
        multiplier = math.ceil(length / len(char))
        separator = char * multiplier
        self.writeln(separator[:self.max_width])

    def write_test_outcome(
        self,
        description: str,
        test_failures: typing.List[TestOutcome],
    ) -> None:
        """Write a test description."""
        description_length = self.max_width - 9
        description = self.fixed_width_text(description, description_length)

        verdict = "[ PASS ]" if not test_failures else "[ FAIL ]"
        description = self.fixed_width_text(description, self.max_width - 8) + verdict

        self.writeln(description)

        if test_failures:
            for _, outcome in test_failures:
                self.write_subtest_failure(outcome)
                self.writeln()
                self.write_separator("-")

            self.writeln()

    def write_subtest_failure(self, outcome: TestOutcome) -> None:
        """Format subtest failure and write it to the stream."""
        self.writeln()
        self.write_separator("-")
        self.writeln("Failing test output:")

        _, exception, _ = outcome
        formatted_exception = ''.join(traceback.format_exception_only(type(exception), exception))
        self.stream.write(textwrap.indent(formatted_exception.rstrip(), prefix="  "))

    def write_section_header(self, section_title: str) -> None:
        """Write a section header, optionally including a subtest result header."""
        title_width = self.max_width - 10
        section_title = self.fixed_width_text(section_title, title_width)

        self.writeln()
        self.write_separator("=")
        self.write(f"{section_title}\n")
        self.write_separator("-")


class QualifierTestResult(unittest.TestResult):
    """A custom test result class used for testing entries for our Code Jam qualifier."""

    def __init__(self, stream: StreamWrapper) -> None:
        super().__init__(stream.stream)
        self.stream = stream

        self.current_testclass = TestClass(None, None)
        self.results = {}

        self.failure_output = None
        self._success = None

    @staticmethod
    def get_description(callable_object: typing.Callable) -> str:
        """Extract a description from the callable by looking at the docstring."""
        if callable_object.__doc__:
            description = callable_object.__doc__.splitlines()[0].rstrip(".!?")
        else:
            description = str(callable_object)
        return description

    def switch_testclass(self, test: unittest.TestCase) -> None:
        """Switch to the new test class and print a section header."""
        test_section = self.get_description(test)
        self.current_testclass = TestClass(type=type(test), name=test_section)

        self.stream.write_section_header(test_section)
        self.results[test_section] = {}

    def startTest(self, test: unittest.TestCase) -> None:
        """Prepare the test phase of an individual test method."""
        super().startTest(test)

        if type(test) != self.current_testclass.type:
            self.switch_testclass(test)

        self.failure_output = []

    def stopTest(self, test: unittest.TestCase) -> None:
        """Finalize the test phase of an individual test method."""
        test_description = test.shortDescription().rstrip(".!?")
        self.results[self.current_testclass.name][test_description] = not self.failure_output
        self.stream.write_test_outcome(test_description, self.failure_output)

    def addError(self, test, err):
        self.failure_output.append((test, err))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.failure_output.append((test, err))

    def addSkip(self, test, reason):
        self.failure_output.append((test, (None, SkippedTest(reason), None)))

    def addSubTest(self, test, subtest, outcome):
        """Process the result of a subTest."""
        super().addSubTest(test, subtest, outcome)
        if outcome:
            self.failure_output.append((subtest, outcome))


def main() -> None:
    """Run an ascii-based test suite."""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromName("test_qualifier")
    runner = QualifierTestRunner()
    runner.run(test_suite)


if __name__ == "__main__":
    main()
