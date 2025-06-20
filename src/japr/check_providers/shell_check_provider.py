from japr.check import Check, CheckProvider, CheckResult, Result, Severity
import japr.util
from git import InvalidGitRepositoryError
from git.repo import Repo
import os


class ShellCheckProvider(CheckProvider):
    def name(self):
        return "Shell"

    def test(self, directory):
        shell_files = japr.util.find_files_with_extensions(
            directory, ["sh", "bash", "zsh", "ksh", "csh", "fish", "ps1", "bat", ""]
        )

        for shell_file in shell_files:
            if os.access(shell_file, os.X_OK):
                with open(shell_file, "r") as f:
                    first_line = f.readline().strip()
                    if not first_line.startswith("#!"):
                        yield CheckResult(
                            "SH001",
                            Result.FAILED,
                            shell_file,
                            "Shell script does not have a shebang",
                        )
                    else:
                        yield CheckResult("SH001", Result.PASSED, shell_file)
        else:
            yield CheckResult("SH001", Result.NOT_APPLICABLE)


    def checks(self):
        return [
            Check(
                "SH001",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team", "personal"],
                "Shell scripts marked as executable should contain a shebang",
                """Shell scripts should start with a shebang (e.g., `#!/bin/bash` or `#!/usr/bin/env bash`) to specify the interpreter that should be used to execute the script. This ensures that the script runs correctly regardless of the user's environment.""",
            ),
        ]

