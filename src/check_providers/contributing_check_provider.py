from check import Check, CheckProvider, CheckResult, Result, Severity
import os


class ContributingCheckProvider(CheckProvider):
    def name(self):
        return "Contributing"

    def test(self, directory):
        yield CheckResult(
            "CT001",
            Result.PASSED
            if any(
                [
                    os.path.isfile(os.path.join(directory, "CONTRIBUTING.md")),
                    os.path.isfile(os.path.join(directory, "CONTRIBUTING")),
                    os.path.isfile(os.path.join(directory, "CONTRIBUTING.txt")),
                ]
            )
            else Result.FAILED,
        )

    def checks(self):
        return [
            Check(
                "CT001",
                Severity.MEDIUM,
                ["open-source"],
                (
                    "Projects should have a CONTRIBUTING.md file describing how to contribute to the project"
                ),
                """Create a CONTRIBUTING.md file in the root of the project and add content to describe to other users how they can contribute to the project in the most helpful way""",
            )
        ]
