# Jamie's Awesome Project Rater
A cross-language tool for rating and enforcing the overall quality of projects by looking at tool & language setup

It's a linter that makes sure you install linters (and some other stuff)

![Screenshot of a report](/screenshot.png)

## Installation
Using pip:
```bash
pip install japr
```

Using [pipx](https://github.com/pypa/pipx) which will get you the latest, bleeding edge version:
```bash
pipx install git+https://github.com/JamJar00/japr
```

Or you can use Docker:
```bash
docker run --rm -v $(pwd):/app jamoyjamie/japr:v0.1.0
```

## Usage
```bash
japr <directory> -t <project-type>
```

For more options:
```bash
japr <directory> [--summary] [--project-type <open-source|inner-source|team|personal>]
```

#### Project Type
To run a check you need to tell Japr about the audience of your projects so it can select a good set of rules to apply. Most personal projects don't need a pull request template for example!

Select one of the following project types and pass on the command line via `-t`/`--project-type` or in the configuration file as in the section below.
| Project Type | Description                                                                                                                                                    |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| open-source  | A comprehensive ruleset for open source projects that are for anyone and everyone that might stumble upon the code                                             |
| inner-source | A comprehensive ruleset for projects that are accessible across an organisation and may be used by other teams (often referred to as 'inner source' projects   |
| team         | A balanced ruleset designed for projects that belong to a single team                                                                                          |
| personal     | A lightweight ruleset designed to tidy up personal projects                                                                                                    |

![Animation of a report and a fix](/animation.gif)

### Configuration
Configuration is done mostly through a `.japr.yaml` file in the root of your repository.
```yaml
# .japr.yaml
projectType: open-source
```
The most useful thing to put in there is the project type so it doesn't need to be specified on the command line each time

#### Suppressing Checks
If you need to suppress a check then you can add an `overrides` second to your configuration file like so:
```yaml
# .japr.yaml
override:
  - id: CI001
    suppress: true
```
Be aware that the project's score is always calculated against the full ruleset no matter what you suppress so that the score is comparable across projects of the same type.

## Score
Japr produces a score for each project between 0 and 5 stars. A project with a 5 star score is very commendable.

This score is always calculated against the full ruleset so is comparable between projects of the same type even if they have different suppressions set.

## Supported Languages
Japr will work for projects of all languages however there are additional checks for the following:
- Python
- C#
- Javascript

The following table tracks the level of support for each language. Many languages also have additional checks not listed.
|                       | Python         | C# | JS        |
|-----------------------|----------------|----|-----------|
| Linter setup          | ✅             | ✅ | ✅        |
| Lock files in Git     | ✅             | ❌ | ✅        |
| Dependency Managers   | Poetry, Pipenv |    | NPM, Yarn |

## Experimental Automatic Fixes
Japr can automatically fix some issues when supplied the `--fix` flag. **This functionality is highly expermental and should never be used on serious project as it could cause serious damage to the project**

## TODO
- Support code blocks in the advice section
- Deploy to Docker Hub
- Tests, always need ~more~ tests
- Allow enabling checks even when project type usually suppresses it
- Allow configuring suppressed rules only for certain files
- Fixes for more checks and stabilise
- Fix not finding git repo if repo root is a parent directory

### Checks
- Check lock files are checked into Git
- Are linters in dev dependencies?
- No TODOs anywhere, they should be tracked in issues
- More languages
- Is it a recognised license? Appropriate for the type of project?
- Copyright headers?
- Code of Conduct file - https://bttger.github.io/contributing-gen-web/

#### Python
- Support Flit & Setuptools as other dependency managers
    https://peps.python.org/pep-0621/
- No Python 2

#### GitHub
- Pull request templates/issue templates should have YAML front matter
- Issue templates should be in the .github folder

#### Sketchy Ideas
- Has git tags for versions?
  - Versions in project files match latest git tag
    - Might need thought for cases where the version has been bumped but the tag hasn't been pushed yet
- Integrate with GitHub?

### Tests
- Git provider
- JS/Python lock files in git

## Rules
