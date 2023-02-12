from japr.check import Check, CheckProvider, CheckFix, CheckResult, Result, Severity
import os


class AddContributorFix(CheckFix):
    def fix(self, directory, _):
        with open(os.path.join(directory, "CONTRIBUTING.md"), 'w') as f:
            # TODO provide a better template like one from https://bttger.github.io/contributing-gen-web/
            f.write("""# Contributing
This is an example contributing document. You should fill this in with guidelines on how to contribute to this project. See https://bttger.github.io/contributing-gen-web/ for a template""")
        return True

    @property
    def success_message(self):
        return "Created a CONTRIBUTING.md file in the root directory from a template. You should add your own content to it."

    @property
    def failure_message(self):
        return "Tried to create a CONTRIBUTING.md file in the root directory but was unable to."


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
            fix=AddContributorFix(),
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
