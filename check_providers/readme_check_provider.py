from check import Check, CheckProvider, CheckResult, Result, Severity
import os


class ReadmeCheckProvider(CheckProvider):
    def test(self, directory):
        if os.path.isfile(directory + "/README.md"):
            readme_path = directory + "/README.md"
        elif os.path.isfile(directory + "/README"):
            readme_path = directory + "/README"
        elif os.path.isfile(directory + "/README.txt"):
            readme_path = directory + "/README.txt"
        else:
            readme_path = None

        yield CheckResult("RE001", Result.PASSED if readme_path is not None else Result.FAILED)

        if readme_path is not None:
            with open(readme_path, 'r') as readme_file:
                content = readme_file.read()

            yield CheckResult("RE002", Result.PASSED if content.find("# Installation") != -1 or content.find("# Setup") != -1 else Result.FAILED)
            yield CheckResult("RE003", Result.PASSED if content.find("# Usage") != -1 else Result.FAILED)
        else:
            yield CheckResult("RE002", Result.PRE_REQUISITE_CHECK_FAILED)
            yield CheckResult("RE003", Result.PRE_REQUISITE_CHECK_FAILED)

    def checks(self):
        return [
            Check(
                "RE001",
                Severity.HIGH,
                ["open-source", "inner-source", "team", "personal"],
                "Projects should have a README.md file describing the project and its use",
                """Create a README.md file in the root of the project and add content to describe to other users (or just your future self) things like:
- Why does this project exist?
- How do I install it?
- How do I use it?
- What configuration can be set?
- How do I build the source code?"""),

            Check(
                "RE002",
                Severity.LOW,
                ["open-source", "inner-source", "team", "personal"],
                "README.md should contain an Installation section",
                """To help users (and your future self) install your project/library you should provide an installation section in your README. Add the following to your readme:

## Installation
1. Do this
2. Now do this"""),

            Check(
                "RE003",
                Severity.LOW,
                ["open-source", "inner-source", "team", "personal"],
                "README.md should contain a Usage section",
                """To help users (and your future self) use your project/library you should provide a usage section in your README. Add the following to your readme:

## Usage
To do this thing:
1. Do this
2. Then run this""")
        ]
