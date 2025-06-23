from japr.check import Check, CheckProvider, CheckResult, Result, Severity
import japr.util
import platform


class ShellCheckProvider(CheckProvider):
    def name(self):
        return "Shell"

    def test(self, directory):
        executable_files = list(japr.util.find_executable_files(directory))
        shebang_files = list(japr.util.find_files_with_shebang(directory))

        # Windows doesn't have a concept of executable files so skip these checks
        if platform.system() == "Windows" and len(executable_files) > 0:
            for executable_file in executable_files:
                yield CheckResult(
                    "SH001", Result.PRE_REQUISITE_CHECK_FAILED, executable_file
                )
        else:
            if len(executable_files) > 0:
                for executable_file in executable_files:
                    if executable_file not in shebang_files:
                        yield CheckResult(
                            "SH001",
                            Result.FAILED,
                            executable_file,
                        )
                    else:
                        yield CheckResult("SH001", Result.PASSED, executable_file)
            else:
                yield CheckResult("SH001", Result.NOT_APPLICABLE)

        if platform.system() == "Windows" and len(shebang_files) > 0:
            for shebang_file in shebang_files:
                yield CheckResult(
                    "SH002", Result.PRE_REQUISITE_CHECK_FAILED, shebang_file
                )
        else:
            if len(shebang_files) > 0:
                for shebang_file in shebang_files:
                    if shebang_file not in executable_files:
                        yield CheckResult(
                            "SH002",
                            Result.FAILED,
                            shebang_file,
                        )
                    else:
                        yield CheckResult("SH002", Result.PASSED, shebang_file)
            else:
                yield CheckResult("SH002", Result.NOT_APPLICABLE)

    def checks(self):
        return [
            Check(
                "SH001",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team", "personal"],
                "Shell scripts marked as executable should contain a shebang",
                """Shell scripts should start with a shebang (e.g., `#!/bin/bash` or `#!/usr/bin/env bash`) to specify the interpreter that should be used to execute the script. This ensures that the script runs correctly regardless of the user's environment.

                This check cannot be run on Windows""",
            ),
            Check(
                "SH002",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team", "personal"],
                "Shell scripts starting with a shebang should be marked as executable",
                """Shell scripts starting with a shebang (e.g., `#!/bin/bash` or `#!/usr/bin/env bash`) are designed to be executable from the command line. On platforms like Linux and OSX these scripts need to be marked as executable.

                 To set the executable flag on the file, use: chmod +x <script_name>

                 This check cannot be run on Windows""",
            ),
        ]
