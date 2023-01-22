from japr.check import Check, CheckProvider, CheckResult, Result, Severity
from git import InvalidGitRepositoryError, Repo
import glob
import os
import json


_linters = [
    "jslint",
    "eslint",
    "jshint",
    "jscs",
    "standard",
]


def _extract_dependencies_from_package_json(file):
    with open(file) as f:
        data = json.load(f)

        try:
            dependencies = [dependency for dependency in data["dependencies"]]
        except KeyError:
            dependencies = []
        try:
            dev_dependencies = [
                dev_dependency for dev_dependency in data["devDependencies"]
            ]
        except KeyError:
            dev_dependencies = []

        return set(dependencies).union(set(dev_dependencies))


class JavascriptCheckProvider(CheckProvider):
    def name(self):
        return "Javascript"

    def test(self, directory):
        package_jsons = glob.glob("**/package.json", recursive=True, root_dir=directory)

        try:
            repo = Repo(directory)
        except InvalidGitRepositoryError:
            repo = None  # Deal with later when we know what checks we're doing

        if len(package_jsons) != 0:
            for package_json in package_jsons:
                # It's bad enough we can't exclude this from the glob, let's not check every packages' package's package.json has a linter
                if "node_modules" in package_json:
                    continue

                dependencies = _extract_dependencies_from_package_json(
                    os.path.join(directory, package_json)
                )
                yield CheckResult(
                    "JS002",
                    Result.PASSED
                    if len(set(_linters).intersection(dependencies))
                    else Result.FAILED,
                    package_json,
                )

                # Check lock file is committed into Git
                if repo is not None:
                    package_lock_file = os.path.join(
                        os.path.split(package_json)[0], "package-lock.json"
                    )
                    yarn_lock_file = os.path.join(
                        os.path.split(package_json)[0], "yarn.lock"
                    )
                    pnpm_lock_file = os.path.join(
                        os.path.split(package_json)[0], "pnpm-lock.yaml"
                    )
                    is_file_committed = any(
                        f.type == "blob"
                        and f.path
                        in [package_lock_file, yarn_lock_file, pnpm_lock_file]
                        for f in repo.tree("HEAD").list_traverse()
                    )
                    yield CheckResult(
                        "JS004",
                        Result.PASSED if is_file_committed else Result.FAILED,
                        package_json,
                    )
                else:
                    yield CheckResult(
                        "JS004",
                        Result.PRE_REQUISITE_CHECK_FAILED,
                        package_json,
                    )
        else:
            yield CheckResult("JS002", Result.NOT_APPLICABLE)
            yield CheckResult("JS004", Result.NOT_APPLICABLE)

    def checks(self):
        return [
            Check(
                "JS002",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team"],
                "Javascript projects should have a linter configured",
                """Javascript projects should have a comprehensive linter configured such as ESLint""",
            ),
            Check(
                "JS004",
                Severity.MEDIUM,
                ["open-source", "inner-source", "team", "personal"],
                "Javascript projects should have their lock files committed into Git",
                """When using a dependency manager for Javascript such as npm, the lock files should be comitted into Git. This ensures that all dependencies of packages are installed at the same version no matter when and on what machine the project is installed.""",
            ),
        ]
