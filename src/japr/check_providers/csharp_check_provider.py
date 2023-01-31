from japr.check import Check, CheckProvider, CheckResult, Result, Severity
import japr.util
import os
import xml.etree.ElementTree as ET


_linters = [
    "StyleCop.Analyzers",
    "SonarAnalyzer.CSharp",
    "Microsoft.CodeAnalysis.NetAnalyzers",
    "Roslynator.Analyzers",
    "Roslynator.CodeAnalysis.Analyzers",
    "Roslynator.Formatting.Analyzers",
]


def _extract_dependencies_from_csproj(file):
    data = ET.parse(file)

    try:
        dependencies = [
            reference.get("Include")
            for reference in data.findall("/ItemGroup/PackageReference")
        ]
    except KeyError:
        dependencies = []

    return set(dependencies)


def _has_enable_net_analyzers_in_csproj(file):
    data = ET.parse(file)

    try:
        # TODO this defaults to true on net5.0 and above
        # TODO consider the EnforceCodeStyleInBuild property too
        properties = data.findall("/PropertyGroup/EnableNETAnalyzers")
        return len(properties) > 0 and all(
            property.text == "true"
            for property in properties
        )
    except KeyError:
        return False


class CSharpCheckProvider(CheckProvider):
    def name(self):
        return "C#"

    def test(self, directory):
        cs_projects = list(japr.util.find_files_with_extension(directory, "csproj"))

        if len(cs_projects) != 0:
            for cs_project in cs_projects:
                dependencies = _extract_dependencies_from_csproj(
                    os.path.join(directory, cs_project)
                )
                has_enable_net_analyzers = _has_enable_net_analyzers_in_csproj(os.path.join(directory, cs_project))
                yield CheckResult(
                    "CS002",
                    Result.PASSED
                    if len(set(_linters).intersection(dependencies)) or has_enable_net_analyzers
                    else Result.FAILED,
                    cs_project,
                )
        else:
            yield CheckResult("CS002", Result.NOT_APPLICABLE)

    def checks(self):
        return [
            Check(
                "CS002",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team"],
                "C# projects should have a linter configured",
                """C# projects should have a comprehensive linter configured such as StyleCop""",
            )
        ]
