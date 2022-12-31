import argparse
from check_providers import check_providers
from check import Result, Severity
import os
import yaml


def check_directory(directory, is_summary=False):
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"'{directory}' is not a valid directory so cannot be checked")
        return

    if os.path.isfile(directory + "/healthcheck.yaml"):
        with open(directory + "/healthcheck.yaml", "r") as f:
            data = yaml.safe_load(f)
            try:
                ignored_checks = [override["id"] for override in data["override"] if override["ignore"]]
            except KeyError:
                ignored_checks = []
    else:
        ignored_checks = []

    issues = []
    for check_provider in check_providers:
        checks = {check.id: check for check in check_provider.checks()}

        results = check_provider.test(directory)
        issues.extend((result, checks[result.id]) for result in results if result.id not in ignored_checks)

    print(f"\033[1m{os.path.basename(directory)}\033[0;0m")
    print("=" * 10)
    for (result, check) in issues:
        if result.result == Result.FAILED:
            severity_color = "\033[1;31m" if check.severity == Severity.HIGH else "\033[1;33m" if check.severity == Severity.MEDIUM else "\033[37m"
            print(f"{severity_color}{check.severity.name.ljust(6)}\033[0;0m - \033[1m{check.id}\033[0;0m {check.reason}")
            if not is_summary:
                print()
                print(check.advice)
                print()
                print("-" * 10)

    print()

    score = int(5 - sum(check.severity.value for (result, check) in issues if result.result == Result.FAILED or result.result == Result.PRE_REQUISITE_CHECK_FAILED) / sum(check.severity.value for (_, check) in issues) * 5)
    print("\033[1mProject score: " + "\U00002B50" * score + "\033[0;0m (out of 5)")

    passed = len([result for (result, _) in issues if result.result == Result.PASSED])
    failed = len([result for (result, _) in issues if result.result == Result.FAILED])
    cannot_run = len([result for (result, _) in issues if result.result == Result.PRE_REQUISITE_CHECK_FAILED])
    print(f"\033[1m\033[1;32mPassed: {passed}\033[0;0m, \033[1m\033[1;31mFailed: {failed}\033[0;0m, \033[1m\033[1;37mCannot Run Yet: {cannot_run}\033[0;0m")

    if score == 5:
        print()
        print("\033[1mCongratulations on a fantastic health-check score \U0001F389\033[0;0m")

    print()


parser = argparse.ArgumentParser(
                    prog='health-check',
                    description='A health check for your projects')

parser.add_argument('directories', nargs="*", help="a directory to scan")
parser.add_argument('-s', '--summary', help="prints results in summary form", action='store_true')

args = parser.parse_args()
for directory in args.directories:
    check_directory(directory, args.summary)
