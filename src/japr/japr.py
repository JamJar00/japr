import argparse
from japr.check_providers import check_providers
from japr.check import Result, Severity
import json
import os
import sys
import time
import yaml


PROJECT_TYPES = ["open-source", "inner-source", "team", "personal"]


def _check_directory(
    directory,
    project_type,
    is_summary=False,
    is_profile=False,
    fix=False,
    is_json=False,
):
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(
            f"'{directory}' is not a valid directory so cannot be checked",
            file=sys.stderr,
        )
        return

    if os.path.isfile(os.path.join(directory, ".japr.yaml")):
        with open(os.path.join(directory, ".japr.yaml"), "r") as f:
            data = yaml.safe_load(f)
            try:
                suppressed_checks = [
                    override["id"]
                    for override in data["override"]
                    if override["suppress"]
                ]
            except KeyError:
                suppressed_checks = []
            if project_type is None:
                try:
                    project_type = data["projectType"]
                except KeyError:
                    project_type = None
    else:
        suppressed_checks = []

    if project_type is None:
        print("No project type specified. You can specify this with the -t flag or add to your .japr.yaml configuration file.", file=sys.stderr)
        return

    if project_type not in PROJECT_TYPES:
        print(
            f"Invalid project type. Must be one of {', '.join(PROJECT_TYPES)}.",
            file=sys.stderr,
        )
        return

    if fix:
        is_summary = True

    issues = []
    for check_provider in check_providers:
        checks = {check.id: check for check in check_provider.checks()}

        results = check_provider.test(directory)

        # results is actually a generator so we can time how long it takes to make each result
        start = time.time()
        for result in results:
            end = time.time()
            try:
                if project_type in checks[result.id].project_types:
                    issues.append((result, checks[result.id], end - start))
            except KeyError:
                raise Exception(
                    f"Check {result.id} is not defined in the"
                    f" {check_provider.name()} check provider but a result was returned"
                    " for it. Ensure the result is returning the correct ID and the"
                    " check is defined correctly in the provider."
                )
            start = time.time()

    sev_bad_checks = sum(
        check.severity.value
        for (result, check, _) in issues
        if result.result == Result.FAILED
        or result.result == Result.PRE_REQUISITE_CHECK_FAILED
    )
    sev_all_checks = sum(check.severity.value for (_, check, _) in issues)
    score = int(5 - sev_bad_checks / sev_all_checks * 5)

    passed = len(
        [
            result
            for (result, _, _) in issues
            if result.result == Result.PASSED and result.id not in suppressed_checks
        ]
    )
    failed = len(
        [
            result
            for (result, _, _) in issues
            if result.result == Result.FAILED and result.id not in suppressed_checks
        ]
    )
    cannot_run = len(
        [
            result
            for (result, _, _) in issues
            if result.result == Result.PRE_REQUISITE_CHECK_FAILED
            and result.id not in suppressed_checks
        ]
    )
    suppressed = len(
        [result for (result, _, _) in issues if result.id in suppressed_checks]
    )

    fixed_results = {}
    if fix:
        for result, check, profile_time in issues:
            if result.result == Result.FAILED and result.fix is not None:
                fixed_results[result] = result.fix.fix(directory, result.file_path)

    if is_json:
        out = {
            "results": [
                {
                    "id": result.id,
                    "result": str(result.result),
                    "filePath": result.file_path,
                    "fixAvailable": result.fix is not None,
                    "severity": str(check.severity),
                    "reason": check.reason,
                    "advice": check.advice,
                    "is_suppressed": result.id in suppressed_checks,
                    "is_fixed": fixed_results[result],
                }
                for (result, check, _) in issues
            ],
            "score": score,
            "passed": passed,
            "failed": failed,
            "cannot_run": cannot_run,
            "suppressed": suppressed,
        }
        print(json.dumps(out, indent=2))
    else:
        for result, check, profile_time in issues:
            if (
                result.result == Result.FAILED and result.id not in suppressed_checks
            ) or is_profile:
                # Build up components then display for code clarity
                if result.result == Result.FAILED:
                    emoji_block = "\N{cross mark}"
                elif result.result == Result.PASSED:
                    emoji_block = "\N{white heavy check mark}"
                elif result.result == Result.PRE_REQUISITE_CHECK_FAILED:
                    emoji_block = "\N{white question mark ornament}"
                else:
                    emoji_block = "\N{heavy minus sign}"

                if check.severity == Severity.HIGH:
                    severity_color = "\033[1;31m"
                elif check.severity == Severity.MEDIUM:
                    severity_color = "\033[1;33m"
                else:
                    severity_color = "\033[37m"

                profile_block = (str(round(profile_time * 1000)) + "ms").ljust(8)

                if result.file_path is not None:
                    file_block = f"[{result.file_path}] "
                else:
                    file_block = ""

                if result.fix is not None:
                    fix_block = f" - A fix is available \N{wrench}"
                else:
                    fix_block = ""

                if is_summary:
                    print(
                        f"{severity_color}{check.severity.name.ljust(6)}\033[0;0m -"
                        f" \033[1m{check.id}\033[0;0m {file_block}{check.reason}"
                        f"{fix_block}"
                    )
                elif is_profile:
                    print(
                        f"{emoji_block} {severity_color}{check.severity.name.ljust(6)}\033[0;0m"
                        f" - {profile_block} - \033[1m{check.id}\033[0;0m"
                        f" {file_block}{check.reason}{fix_block}"
                    )
                else:
                    print(
                        f"{severity_color}{check.severity.name.ljust(6)}\033[0;0m -"
                        f" \033[1m{check.id}\033[0;0m {file_block}{check.reason}"
                        f"{fix_block}"
                    )
                    print()
                    print(check.advice)
                    print()
                    print("-" * 10)

        print()
        print(
            "\033[1mProject score: "
            + "\N{glowing star}" * score
            + "\N{heavy minus sign}" * (5 - score)
            + "\033[0;0m"
        )

        print(
            f"\033[1m\033[1;32mPassed: {passed}\033[0;0m, \033[1m\033[1;31mFailed:"
            f" {failed}\033[0;0m, \033[1m\033[1;37mCannot Run Yet: {cannot_run}, Suppressed"
            f" {suppressed}\033[0;0m"
        )

        if score == 5:
            print()
            print("\033[1mCongratulations on a fantastic score \U0001F389\033[0;0m")

        if fix:
            print()
            for result in fixed_results:
                if fixed_results[result]:
                    print(f"\N{white heavy check mark} {result.fix.success_message}")
                else:
                    print(f"\N{cross mark} {result.fix.failure_message}")

        print()

    if fix:
        return all(fixed_results[result] for result in fixed_results)
    else:
        return failed == 0


def cli(args=None):
    parser = argparse.ArgumentParser(
        prog="japr",
        description=(
            "A cross-language tool for rating the overall quality of open source,"
            " commercial and personal projects"
        ),
    )

    parser.add_argument("directory", help="the directory to scan")
    parser.add_argument(
        "-t",
        "--project-type",
        help="the type of project being scanned",
        choices=PROJECT_TYPES,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--profile", help="times how long each check takes to run", action="store_true"
    )
    group.add_argument(
        "-s", "--summary", help="prints results in summary form", action="store_true"
    )
    group.add_argument(
        "--fix", help="experimentally try to fix issues found", action="store_true"
    )
    group.add_argument("--json", help="output results as JSON", action="store_true")

    args = parser.parse_args(args)
    if _check_directory(
        args.directory,
        args.project_type,
        args.summary,
        args.profile,
        args.fix,
        args.json,
    ):
        quit(0)
    else:
        quit(1)
