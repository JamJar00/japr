from check import Check, CheckProvider, CheckResult, Result, Severity
from git import InvalidGitRepositoryError, Repo
import glob
import toml
import os


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
        setup_pys = glob.glob("**/setup.py", recursive=True, root_dir=directory)
        setup_cfgs = glob.glob("**/setup.cfg", recursive=True, root_dir=directory)

        try:
            repo = Repo(directory)
        except InvalidGitRepositoryError:
            repo = None  # Deal with later when we know what checks we're doing

        if len(requirements_txts) != 0:
            for requirements_txt in requirements_txts:
                yield CheckResult("PY001", Result.FAILED, requirements_txt)
        else:
            yield CheckResult("PY001", Result.NOT_APPLICABLE)

        if len(pyproject_tomls) != 0 or len(pipfiles) != 0:
            for pyproject_toml in pyproject_tomls:
                dependencies = _extract_dependencies_from_pyproject(
                    os.path.join(directory, pyproject_toml)
                )
                yield CheckResult(
                    "PY002",
                    Result.PASSED
                    if len(set(_linters).intersection(dependencies))
                    else Result.FAILED,
                    pyproject_toml,
                )

                # Check lock file is committed into Git
                if repo is not None:
                    lock_file = os.path.join(
                        os.path.split(pyproject_toml)[0], "poetry.lock"
                    )
                    is_file_committed = any(
                        f.type == "blob" and f.path == lock_file
                        for f in repo.tree("HEAD").list_traverse()
                    )
                    yield CheckResult(
                        "PY004",
                        Result.PASSED if is_file_committed else Result.FAILED,
                        pyproject_toml,
                    )
                else:
                    yield CheckResult(
                        "PY004",
                        Result.PRE_REQUISITE_CHECK_FAILED,
                        pyproject_toml,
                    )

            for pipfile in pipfiles:
                dependencies = _extract_dependencies_from_pipfile(
                    os.path.join(directory, pipfile)
                )
                yield CheckResult(
                    "PY002",
                    Result.PASSED
                    if len(set(_linters).intersection(dependencies))
                    else Result.FAILED,
                    pipfile,
                )

                # Check lock file is committed into Git
                if repo is not None:
                    lock_file = pipfile + ".lock"
                    is_file_committed = any(
                        f.type == "blob" and f.path == lock_file
                        for f in repo.tree("HEAD").list_traverse()
                    )
                    yield CheckResult(
                        "PY004",
                        Result.PASSED if is_file_committed else Result.FAILED,
                        pipfile,
                    )
                else:
                    yield CheckResult(
                        "PY004",
                        Result.PRE_REQUISITE_CHECK_FAILED,
                        pipfile,
                    )
        else:
            yield CheckResult("PY002", Result.NOT_APPLICABLE)
            yield CheckResult("PY004", Result.NOT_APPLICABLE)

        if len(setup_pys) != 0 or len(setup_cfgs) != 0:
            for setup_py in setup_pys:
                yield CheckResult("PY003", Result.FAILED, setup_py)
            for setup_cfg in setup_cfgs:
                yield CheckResult("PY003", Result.FAILED, setup_cfg)
        else:
            yield CheckResult("PY003", Result.NOT_APPLICABLE)

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
            Check(
                "PY003",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team", "personal"],
                "Python projects should prefer a build system to setup.py/setup.cfg",
                """Python is moving towards using more intelligent build systems like Poetry or pipenv to manage dependencies. Consider switching from a setup.py or setup.cfg file to one of these tools.""",
            ),
            Check(
                "PY004",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team", "personal"],
                "Python projects using a dependency manager should have their lock files committed into Git",
                """When using a dependency manager for Python such as Poetry, the lock files should be comitted into Git. This ensures that all dependencies of packages are installed at the same version no matter when and on what machine the project is installed.""",
            ),
        ]
