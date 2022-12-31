from check import Check, CheckProvider, CheckResult, Result, Severity
import glob
import os
import toml


def _extract_dependencies_from_pyproject(directory):
    with open(directory + "/pyproject.toml", "r") as f:
        data = toml.load(f)

        try:
            dependencies = data["tool"]["poetry"]["dependencies"].keys()
        except KeyError:
            dependencies = []

        try:
            dev_dependencies = data["tool"]["poetry"]["group"]["dev"]["dependencies"].keys()
        except KeyError:
            dev_dependencies = []

        return set(dependencies).union(set(dev_dependencies))


def _extract_dependencies_from_pipfile(directory):
    with open(directory + "/Pipfile", "r") as f:
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
    def test(self, directory):
        if len(glob.glob('**/*.py', recursive=True, root_dir=directory)) == 0:
            yield CheckResult("PY001", Result.NOT_APPLICABLE)
            yield CheckResult("PY002", Result.NOT_APPLICABLE)
            yield CheckResult("PY003", Result.NOT_APPLICABLE)
            return
        
        yield CheckResult("PY001", Result.PASSED if not os.path.isfile(directory + "/requirements.txt") else Result.FAILED)
        yield CheckResult("PY002", Result.PASSED if any([os.path.isfile(directory + "/Pipfile"), os.path.isfile(directory + "/pyproject.toml"), os.path.isfile(directory + "/requirements.txt")]) else Result.FAILED)

        if os.path.isfile(directory + "/pyproject.toml"):
            dependencies = _extract_dependencies_from_pyproject(directory)
        elif os.path.isfile(directory + "/Pipfile"):
            dependencies = _extract_dependencies_from_pipfile(directory)
        # elif os.path.isfile(directory + "/requirements.txt"):
        #     dependencies = _extract_dependencies_from_requirements(directory)
        else:
            dependencies = []
        yield CheckResult("PY003", Result.PASSED if len(set(["pylama", "flake8"]).intersection(dependencies)) else Result.FAILED)

    def checks(self):
        return [
                Check(
                    "PY001",
                    Severity.MEDIUM,
                    "Python projects should prefer a build system to a requirements.txt",
                    """Python is moving towards using more intelligent build systems like Poetry or pipenv to manage dependencies. Consider switching from a requirements.txt file to one of these tools."""),

                Check(
                    "PY002",
                    Severity.LOW,
                    "Python projects should have a dependency manager",
                    """Python projects should have some way of tracking dependencies for the project, such as a pyproject.toml with Poetry or a Pipfile, even if they have no dependencies.

Setup a tool like Poetry or pipenv."""),

                Check(
                    "PY003",
                    Severity.MEDIUM,
                    "Python projects should have a linter configured",
                    """Python projects should have a comprehensive linter configured such as Pylama or Flake8""")
               ]
