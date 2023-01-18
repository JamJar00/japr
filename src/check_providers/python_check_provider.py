from check import Check, CheckProvider, CheckResult, Result, Severity
import glob
import toml


# Sourced from https://github.com/vintasoftware/python-linters-and-code-analysis
_linters = [
    "coala-bears",
    "yala",
    "prospector",
    "pylama",
    "ciocheck",
    "wemake-python-styleguide",
    "flake8",
    "black",
]


def _extract_dependencies_from_pyproject(path):
    with open(path, "r") as f:
        data = toml.load(f)

        try:
            dependencies = data["tool"]["poetry"]["dependencies"].keys()
        except KeyError:
            dependencies = []

        try:
            dev_dependencies = data["tool"]["poetry"]["group"]["dev"][
                "dependencies"
            ].keys()
        except KeyError:
            dev_dependencies = []

        return set(dependencies).union(set(dev_dependencies))


def _extract_dependencies_from_pipfile(path):
    with open(path, "r") as f:
        data = toml.load(f)

        try:
            dependencies = data["packages"].keys()
        except KeyError:
            dependencies = []

        try:
            dev_dependencies = data["dev-packages"].keys()
        except KeyError:
            dev_dependencies = []

        return set(dependencies).union(set(dev_dependencies))


class PythonCheckProvider(CheckProvider):
    def name(self):
        return "Python"

    def test(self, directory):
        requirements_txts = glob.glob(
            "**/requirements.txt", recursive=True, root_dir=directory
        )
        pyproject_tomls = glob.glob(
            "**/pyproject.toml", recursive=True, root_dir=directory
        )
        pipfiles = glob.glob("**/Pipfile", recursive=True, root_dir=directory)

        for requirements_txt in requirements_txts:
            yield CheckResult("PY001", Result.FAILED, requirements_txt)
        else:
            yield CheckResult("PY001", Result.NOT_APPLICABLE)

        if len(pyproject_tomls) != 0 or len(pipfiles) != 0:
            for pyproject_toml in pyproject_tomls:
                dependencies = _extract_dependencies_from_pyproject(
                    directory + "/" + pyproject_toml
                )
                yield CheckResult(
                    "PY002",
                    Result.PASSED
                    if len(set(_linters).intersection(dependencies))
                    else Result.FAILED,
                    pyproject_toml,
                )

            for pipfile in pipfiles:
                dependencies = _extract_dependencies_from_pipfile(
                    directory + "/" + pipfile
                )
                yield CheckResult(
                    "PY002",
                    Result.PASSED
                    if len(set(_linters).intersection(dependencies))
                    else Result.FAILED,
                    pipfile,
                )
        else:
            yield CheckResult("PY002", Result.NOT_APPLICABLE)

    def checks(self):
        return [
            Check(
                "PY001",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team", "personal"],
                "Python projects should prefer a build system to a requirements.txt",
                """Python is moving towards using more intelligent build systems like Poetry or pipenv to manage dependencies. Consider switching from a requirements.txt file to one of these tools.""",
            ),
            Check(
                "PY002",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team"],
                "Python projects should have a linter configured",
                """Python projects should have a comprehensive linter configured such as Pylama""",
            ),
        ]
