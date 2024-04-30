"""
This script is designed to easily generate the documentation from the checks as configured in code
"""

from japr.check_providers import check_providers


def generate():
    for check_provider in check_providers:
        checks = check_provider.checks()
        checks.sort(key=lambda s: s.id)

        print(f"### {check_provider.name()}")
        print("| ID | Severity | Enabled for Project Types | Description | Advice |")
        print("|----|----------|---------------------------|-------------|--------|")
        for check in checks:
            advice = check.advice.replace("\n", "</br>")
            severity = check.severity.name.title()
            print(
                f"| {check.id} | {severity} | {', '.join(check.project_types)} |"
                f" {check.reason} | {advice} |"
            )
        print()


if __name__ == "__main__":
    generate()
