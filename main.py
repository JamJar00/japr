import argparse
from check_providers import check_providers
from check import Result, Severity
import os
import yaml


PROJECT_TYPES = ["open-source", "inner-source", "team", "personal"]


def check_directory(directory, project_type, is_summary=False):
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"'{directory}' is not a valid directory so cannot be checked")
        return

    if os.path.isfile(directory + "/.japr.yaml"):
        with open(directory + "/.japr.yaml", "r") as f:
            data = yaml.safe_load(f)
            try:
                ignored_checks = [override["id"] for override in data["override"] if override["ignore"]]
            except KeyError:
                ignored_checks = []
            if project_type is None:
                try:
                    project_type = data["projectType"]
                except KeyError:
                    project_type = None
    else:
        ignored_checks = []

    if project_type is None:
        raise Exception("No project type specified")

    if project_type not in PROJECT_TYPES:
        raise Exception("Invalid project type. Must be one of " + ", ".join(PROJECT_TYPES))

    issues = []
    for check_provider in check_providers:
        checks = {check.id: check for check in check_provider.checks()}

        results = check_provider.test(directory)
        issues.extend((result, checks[result.id]) for result in results if project_type in checks[result.id].project_types)

    # TODO Group issues by ID for multiple files

    print(f"\033[1m{os.path.basename(directory)}\033[0;0m")
    print("=" * 10)
    for (result, check) in issues :
        if result.result == Result.FAILED and result.id not in ignored_checks:
            severity_color = "\033[1;31m" if check.severity == Severity.HIGH else "\033[1;33m" if check.severity == Severity.MEDIUM else "\033[37m"
            if result.file_path is not None:
                print(f"{severity_color}{check.severity.name.ljust(6)}\033[0;0m - \033[1m{check.id}\033[0;0m [{result.file_path}] {check.reason}")
            else:
                print(f"{severity_color}{check.severity.name.ljust(6)}\033[0;0m - \033[1m{check.id}\033[0;0m {check.reason}")
            if not is_summary:
                print()
                print(check.advice)
                print()
                print("-" * 10)

    print()

    score = int(5 - sum(check.severity.value for (result, check) in issues if result.result == Result.FAILED or result.result == Result.PRE_REQUISITE_CHECK_FAILED) / sum(check.severity.value for (_, check) in issues) * 5)
    print("\033[1mProject score: " + "\U00002B50" * score + "\033[0;0m (out of 5)")

    passed = len([result for (result, _) in issues if result.result == Result.PASSED and result.id not in ignored_checks])
    failed = len([result for (result, _) in issues if result.result == Result.FAILED and result.id not in ignored_checks])
    cannot_run = len([result for (result, _) in issues if result.result == Result.PRE_REQUISITE_CHECK_FAILED and result.id not in ignored_checks])
    suppressed = len([result for (result, _) in issues if result.id in ignored_checks])
    print(f"\033[1m\033[1;32mPassed: {passed}\033[0;0m, \033[1m\033[1;31mFailed: {failed}\033[0;0m, \033[1m\033[1;37mCannot Run Yet: {cannot_run}, Suppressed {suppressed}\033[0;0m")

    if score == 5:
        print()
        print("\033[1mCongratulations on a fantastic score \U0001F389\033[0;0m")

    print()

    return len([result for (result, _) in issues if result.result == Result.FAILED and result.id not in ignored_checks]) == 0

parser = argparse.ArgumentParser(
                    prog='japr',
                    description='A cross-language tool for rating the overall quality of open source, commercial and personal projects')

parser.add_argument('directory', help="the directory to scan")
parser.add_argument('-s', '--summary', help="prints results in summary form", action='store_true')
parser.add_argument('-t', '--project-type', help="the type of project being scanned", choices=PROJECT_TYPES)

args = parser.parse_args()
if check_directory(args.directory, args.project_type, args.summary):
    quit(0)
else:
    quit(1)
