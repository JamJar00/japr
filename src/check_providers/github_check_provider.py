from check import Check, CheckProvider, CheckResult, Result, Severity
from git import InvalidGitRepositoryError, Repo
import os


class GitHubCheckProvider(CheckProvider):
    def name(self):
        return "GitHub"

    def test(self, directory):
        try:
            repo = Repo(directory)
            github_is_origin = ("origin" in repo.remotes and "github" in repo.remote("origin").url)
        except InvalidGitRepositoryError:
            github_is_origin = False

        if not github_is_origin:
            yield CheckResult("GH001", Result.NOT_APPLICABLE)
            yield CheckResult("GH002", Result.NOT_APPLICABLE)
            return

        # https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates
        has_issue_template = any([
            os.path.isfile(directory + "/issue_template"),
            os.path.isfile(directory + "/issue_template.md"),
            os.path.isfile(directory + "/issue_template.yml"),
            os.path.isfile(directory + "/docs/issue_template"),
            os.path.isfile(directory + "/docs/issue_template.md"),
            os.path.isfile(directory + "/docs/issue_template.yml"),
            os.path.isfile(directory + "/.github/issue_template"),
            os.path.isfile(directory + "/.github/issue_template.md"),
            os.path.isfile(directory + "/.github/issue_template.yml"),
            os.path.isdir(directory + "/issue_template"),
            os.path.isdir(directory + "/docs/issue_template"),
            os.path.isdir(directory + "/.github/issue_template")
        ])
        # https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
        has_pull_request_template = any([
            os.path.isfile(directory + "/pull_request_template"),
            os.path.isfile(directory + "/pull_request_template.md"),
            os.path.isfile(directory + "/docs/pull_request_template"),
            os.path.isfile(directory + "/docs/pull_request_template.md"),
            os.path.isfile(directory + "/.github/pull_request_template"),
            os.path.isfile(directory + "/.github/pull_request_template.md"),
            os.path.isdir(directory + "/pull_request_template"),
            os.path.isdir(directory + "/docs/pull_request_template"),
            os.path.isdir(directory + "/.github/pull_request_template")
        ])

        yield CheckResult("GH001", Result.PASSED if has_issue_template else Result.FAILED)
        yield CheckResult("GH002", Result.PASSED if has_pull_request_template else Result.FAILED)

    def checks(self):
        return [
                Check(
                    "GH001",
                    Severity.LOW,
                    ["open-source", "inner-source"],
                    "GitHub projects should have an issue template",
                    """To help users create issues that are useful for you an issue template is recommended.

Create a .github/issue_template.md file and fill it with a template for users to use when filing issues.
See https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates"""),

                Check(
                    "GH002",
                    Severity.LOW,
                    ["open-source", "inner-source"],
                    "GitHub projects should have a pull request template",
                    """To help users create pull requests that are useful for you a pull request template is recommended.

Create a .github/pull_request_template.md file and fill it with a template for users to use when filing pull requests
See https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository""")
               ]
