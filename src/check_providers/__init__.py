from check_providers.readme_check_provider import ReadmeCheckProvider
from check_providers.license_check_provider import LicenseCheckProvider
from check_providers.git_check_provider import GitCheckProvider
from check_providers.ci_check_provider import CiCheckProvider
from check_providers.python_check_provider import PythonCheckProvider
from check_providers.github_check_provider import GitHubCheckProvider
from check_providers.csharp_check_provider import CSharpCheckProvider
from check_providers.contributing_check_provider import ContributingCheckProvider
from check_providers.javascript_check_provider import JavascriptCheckProvider

check_providers = [
    ReadmeCheckProvider(),
    LicenseCheckProvider(),
    GitCheckProvider(),
    CiCheckProvider(),
    PythonCheckProvider(),
    GitHubCheckProvider(),
    CSharpCheckProvider(),
    ContributingCheckProvider(),
    JavascriptCheckProvider(),
]
