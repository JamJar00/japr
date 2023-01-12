from check import Check, CheckProvider, CheckResult, Result, Severity
import os


class CiCheckProvider(CheckProvider):
    def test(self, directory):
        if os.path.isfile(directory + "/.gitlab-ci.yml"):
            ci_path = directory + "/.gitlab-ci.yml"
        elif os.path.isfile(directory + "/.travis.yml"):
            ci_path = directory + "/travis.yml"
        elif os.path.isfile(directory + "/appveyor.yml"):
            ci_path = directory + "/appveyor.yml"
        elif os.path.isfile(directory + "/.appveyor.yml"):
            ci_path = directory + "/.appveyor.yml"
        elif os.path.isfile(directory + "/circle.yml"):
            ci_path = directory + "/circle.yml"
        elif os.path.isfile(directory + "/.circleci/config.yml"):
            ci_path = directory + "/.circleci/config.yml"
        elif os.path.isfile(directory + "/Jenkinsfile"):
            ci_path = directory + "/Jenkinsfile"
        elif os.path.isfile(directory + "/.drone.yml"):
            ci_path = directory + "/.drone.yml"
        elif os.path.isdir(directory + "/.github/workflows/"):
            ci_path = directory + "/.github/workflows/"
        elif os.path.isfile(directory + "/azure-pipelines.yml"):
            ci_path = directory + "/azure-pipelines.yml"
        else:
            ci_path = None

        yield CheckResult("CI001", Result.PASSED if ci_path is not None else Result.FAILED)

    def checks(self):
        return [
                Check(
                    "CI001",
                    Severity.MEDIUM,
                    ["open-source", "inner-source", "team", "personal"],
                    "Projects should define a CI/CD pipeline to ensure code builds and works correctly",
                    """Consider creating a CI/CD pipeine for this project using a tool like GitHub Actions. A typical CI/CD pipeline should:
- Lint the code
- Build the code
- Run all tests
- Deploy any built artifacts like NuGet packages/PyPI packages

If at any point a step fails it should block the build""")
               ]
