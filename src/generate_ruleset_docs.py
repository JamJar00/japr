"""
This script is designed to easily generate the documentation from the checks as configured in code
"""
from check_providers import check_providers

checks = []
for check_provider in check_providers:
    for check in check_provider.checks():
        checks.append(check)

checks.sort(key=lambda s: s.id)

print("| ID | Severity | Enabled for Project Types | Description | Advice |")
print("|----|----------|---------------------------|-------------|--------|")
for check in checks:
    advice = check.advice.replace("\n", "</br>")
    severity = check.severity.name.title()
    print(
        f"| {check.id} | {severity} | {', '.join(check.project_types)} |"
        f" {check.reason} | {advice} |"
    )
