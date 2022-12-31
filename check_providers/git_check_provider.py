from check import Check, CheckProvider, CheckResult, Result, Severity
from git import InvalidGitRepositoryError, Repo
import os


class GitCheckProvider(CheckProvider):
    def test(self, directory):
        try:
            repo = Repo(directory)
            yield CheckResult("GI001", Result.PASSED)

            yield CheckResult("GI002", Result.PASSED if "origin" in repo.remotes else Result.FAILED)
            yield CheckResult("GI003", Result.PASSED if "master" not in repo.heads else Result.FAILED)
            yield CheckResult("GI004", Result.PASSED if os.path.isfile(directory + "/.gitignore") else Result.FAILED)
        except InvalidGitRepositoryError:
            yield CheckResult("GI001", Result.FAILED)
            yield CheckResult("GI002", Result.PRE_REQUISITE_CHECK_FAILED)
            yield CheckResult("GI003", Result.PRE_REQUISITE_CHECK_FAILED)
            yield CheckResult("GI004", Result.PRE_REQUISITE_CHECK_FAILED)

    def checks(self):
        return [
            Check(
                "GI001",
                Severity.HIGH,
                "Projects should be tracked in Git version control",
                """All projects, even the smallest personal projects benefit from being tracked in Git as it provides branch management, backups and history to your project.

Run `git init` in this project to setup Git and then make a commit"""),

            Check(
                "GI002",
                Severity.HIGH,
                "Projects in Git should have a remote copy in origin",
                """This project does not have a Git remote named 'origin' which suggests there is no backup copy of the project should it be lost.

Setup a Git repository on your favourite Git service (e.g. GitHub) and follow the instructions to add a remote to an existing project. The instructions will likely look like:

git remote add origin <your url>
git push origin master"""),

            Check(
                "GI003",
                Severity.HIGH,
                "Projects in Git should switch from a 'master' branch to a 'main' branch",
                """This project has a branch named 'master' however it is now recommended to use a branch named 'main' to avoid culturally inappropriate language.

You can switch your primary branch using:

git checkout master
git pull origin master
git switch -c main
git push origin main
git branch -d master
git push :master

You may also need to make changes in your remote to change the default branch"""),

            Check(
                "GI004",
                Severity.LOW,
                "Projects in Git should have a .gitignore file",
                """.gitignore files help you avoid committing unwanted files into Git such as binaries or build artifacts. You should create a .gitignore file for this project.

You can find comprehensive examples for your chosen language here https://github.com/github/gitignore""")
        ]
