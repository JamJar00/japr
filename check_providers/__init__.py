from check_providers.readme_check_provider import ReadmeCheckProvider
from check_providers.license_check_provider import LicenseCheckProvider
from check_providers.git_check_provider import GitCheckProvider
from check_providers.ci_check_provider import CiCheckProvider

check_providers = [
    ReadmeCheckProvider(),
    LicenseCheckProvider(),
    GitCheckProvider(),
    CiCheckProvider()
]
