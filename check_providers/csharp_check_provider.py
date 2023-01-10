from check import Check, CheckProvider, CheckResult, Result, Severity
import glob
import xml.etree.ElementTree as ET


_linters = ["StyleCop.Analyzers", "SonarAnalyzer.CSharp", "Microsoft.CodeAnalysis.NetAnalyzers", "Roslynator.Analyzers", "Roslynator.CodeAnalysis.Analyzers", "Roslynator.Formatting.Analyzers"]


def _extract_dependencies_from_csproj(file):
    data = ET.parse(file)

    try:
        dependencies = [reference.get("Include") for reference in data.findall("/ItemGroup/PackageReference")]
    except KeyError:
        dependencies = []

    return set(dependencies)


class CSharpCheckProvider(CheckProvider):
    def test(self, directory):
        cs_projects = glob.glob("**/*.csproj", recursive=True, root_dir=directory)

        if len(glob.glob('**/*.cs', recursive=True, root_dir=directory)) == 0:
            yield CheckResult("CS003", Result.NOT_APPLICABLE)

        for cs_project in cs_projects:
            dependencies = _extract_dependencies_from_csproj(directory + "/" + cs_project)
            # TODO support EnableNetAnalyzers property
            yield CheckResult("CS003", Result.PASSED if len(set(_linters).intersection(dependencies)) else Result.FAILED, cs_project)

    def checks(self):
        return [
            Check(
                "CS003",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team"],
                "C# projects should have a linter configured",
                """C# projects should have a comprehensive linter configured such as StyleCop""")
           ]
