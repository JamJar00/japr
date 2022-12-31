from check import Check, CheckProvider, CheckResult, Result, Severity
from git import InvalidGitRepositoryError, Repo
import os


class GitHubCheckProvider(CheckProvider):
    def test(self, directory):
        try:
            repo = Repo(directory)
            github_is_origin = ("origin" in repo.remotes and "github" in repo.remote("origin").url)
        except InvalidGitRepositoryError:
            github_is_origin = False

        if not os.path.isdir(".github") and not github_is_origin:
            yield CheckResult("GH001", Result.NOT_APPLICABLE)
            yield CheckResult("GH002", Result.NOT_APPLICABLE)
            return

        yield CheckResult("GH001", Result.PASSED if any([os.path.isfile(directory + "/.github/ISSUE_TEMPLATE"), os.path.isfile(directory + "/.github/ISSUE_TEMPLATE.md"), os.path.isdir(directory + "/.github/ISSUE_TEMPLATE")]) else Result.FAILED)
        yield CheckResult("GH002", Result.PASSED if any([os.path.isfile(directory + "/.github/PULL_REQUEST_TEMPLATE"), os.path.isfile(directory + "/.github/PULL_REQUEST_TEMPLATE.md"), os.path.isdir(directory + "/.github/PULL_REQUEST_TEMPLATE")]) else Result.FAILED)

    def checks(self):
        return [
                Check(
                    "GH001",
                    Severity.LOW,
                    "GitHub projects should have an issue template",
                    """To help users create issues that are useful for you an issue template is recommended.

Create a .github/ISSUE_TEMPLATE.md file and fill it with a tempate for users to use when filing issues"""),

                Check(
                    "GH002",
                    Severity.LOW,
                    "GitHub projects should have a pull request template",
                    """To help users create pull requests that are useful for you a pull request template is recommended.

Create a .github/PULL_REQUEST_TEMPLATE.md file and fill it with a tempate for users to use when filing pull requests""")
               ]
