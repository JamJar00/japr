from japr.check import Check, CheckProvider, CheckFix, CheckResult, Result, Severity
from git import InvalidGitRepositoryError
from git.repo import Repo
import japr.template_util
import os


class AddIssueTemplateFix(CheckFix):
    def fix(self, directory, _):
        os.makedirs(os.path.join(directory, ".github/ISSUE_TEMPLATE"), exist_ok=True)
        with open(os.path.join(directory, ".github/ISSUE_TEMPLATE/bug.md"), "w") as f:
            f.write(
                japr.template_util.template("bug_report_issue_template.md", directory)
            )
        with open(
            os.path.join(directory, ".github/ISSUE_TEMPLATE/feature_request.md"), "w"
        ) as f:
            f.write(
                japr.template_util.template(
                    "feature_request_issue_template.md", directory
                )
            )
        return True

    @property
    def success_message(self):
        return (
            "Created issue templates at .github/ISSUE_TEMPLATE/bug_report.md and"
            " .github/ISSUE_TEMPLATE/feature_request.md from a template. You should add"
            " your own content to it."
        )

    @property
    def failure_message(self):
        return (
            "Tried to create an issue template at .github/ISSUE_TEMPLATE/bug_report.md"
            " and .github/ISSUE_TEMPLATE/feature_request.md but was unable to."
        )


class AddPullRequestTemplateFix(CheckFix):
    def fix(self, directory, _):
        os.makedirs(os.path.join(directory, ".github"), exist_ok=True)
        with open(
            os.path.join(directory, ".github/pull_request_template.md"), "w"
        ) as f:
            f.write(japr.template_util.template("pull_request_template.md", directory))
        return True

    @property
    def success_message(self):
        return (
            "Created an issue template at .github/pull_request_template.md from a"
            " template. You should add your own content to it."
        )

    @property
    def failure_message(self):
        return (
            "Tried to create an issue template at .github/pull_request_template.md but"
            " was unable to."
        )


class GitHubCheckProvider(CheckProvider):
    def name(self):
        return "GitHub"

    def test(self, directory):
        try:
            repo = Repo(directory, search_parent_directories=True)
            github_is_origin = (
                "origin" in repo.remotes and "github" in repo.remote("origin").url
            )
        except InvalidGitRepositoryError:
            github_is_origin = False

        if not github_is_origin:
            yield CheckResult("GH001", Result.NOT_APPLICABLE)
            yield CheckResult("GH002", Result.NOT_APPLICABLE)
            return

        # https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates
        has_issue_template = any(
            [
                os.path.isfile(os.path.join(directory, "issue_template")),
                os.path.isfile(os.path.join(directory, "issue_template.md")),
                os.path.isfile(os.path.join(directory, "issue_template.yml")),
                os.path.isfile(os.path.join(directory, "docs/issue_template")),
                os.path.isfile(os.path.join(directory, "docs/issue_template.md")),
                os.path.isfile(os.path.join(directory, "docs/issue_template.yml")),
                os.path.isfile(os.path.join(directory, ".github/issue_template")),
                os.path.isfile(os.path.join(directory, ".github/issue_template.md")),
                os.path.isfile(os.path.join(directory, ".github/issue_template.yml")),
                os.path.isdir(os.path.join(directory, "issue_template")),
                os.path.isdir(os.path.join(directory, "docs/issue_template")),
                os.path.isdir(os.path.join(directory, ".github/issue_template")),
            ]
        )
        # https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
        has_pull_request_template = any(
            [
                os.path.isfile(os.path.join(directory, "pull_request_template")),
                os.path.isfile(os.path.join(directory, "pull_request_template.md")),
                os.path.isfile(os.path.join(directory, "docs/pull_request_template")),
                os.path.isfile(
                    os.path.join(directory, "docs/pull_request_template.md")
                ),
                os.path.isfile(
                    os.path.join(directory, ".github/pull_request_template")
                ),
                os.path.isfile(
                    os.path.join(directory, ".github/pull_request_template.md")
                ),
                os.path.isdir(os.path.join(directory, "pull_request_template")),
                os.path.isdir(os.path.join(directory, "docs/pull_request_template")),
                os.path.isdir(os.path.join(directory, ".github/pull_request_template")),
            ]
        )

        yield CheckResult(
            "GH001",
            Result.PASSED if has_issue_template else Result.FAILED,
            fix=AddIssueTemplateFix(),
        )
        yield CheckResult(
            "GH002",
            Result.PASSED if has_pull_request_template else Result.FAILED,
            fix=AddPullRequestTemplateFix(),
        )

    def checks(self):
        return [
            Check(
                "GH001",
                Severity.LOW,
                ["open-source", "inner-source"],
                "GitHub projects should have an issue template",
                """To help users create issues that are useful for you an issue template is recommended.

Create a .github/issue_template.md file and fill it with a template for users to use when filing issues.
See https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates""",
            ),
            Check(
                "GH002",
                Severity.LOW,
                ["open-source", "inner-source"],
                "GitHub projects should have a pull request template",
                """To help users create pull requests that are useful for you a pull request template is recommended.

Create a .github/pull_request_template.md file and fill it with a template for users to use when filing pull requests
See https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository""",
            ),
        ]
