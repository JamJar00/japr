# Jamie's Awesome Project Rater
A cross-language tool for rating the overall quality of open source, commercial and personal projects

![Screenshot of a report](/screenshot.png)

## Installation
TODO

## Usage
```bash
japr <directory>
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
    ignore: true
```
Be aware that the project's score is always calculated against the full ruleset no matter what you suppress so that the score is comparable across projects of the same type.

## Score
Japr produces a score for each project between 0 and 5 stars. A project with a 5 star score is very commendable.

This score is always calculated against the full ruleset so is comparable between projects of the same type even if they have different suppressions set.

## Supported Languages
Japr will work for projects of all languages however there are additional checks for the following:
- Python
- C#

The following table tracks the level of support for each language. Many languages also have additional checks not listed.
|                   | Python    | C# |
|-------------------|-----------|----|
| Linter setup      | ✅        | ✅ |
| Lock files in Git | ✅        | ❌ |

## TODO
- Support code blocks in the advice section
- Fix linting
- Deploy to Docker Hub
- Deploy to PyPi
- Tests, always need ~more~ tests

### Checks
- Audit all checks
- Check lock files are checked into Git
- No TODOs anywhere, they should be tracked in issues
- More languages
- Is it a recognised license? Appropriate for the type of project?

#### Python
- Support Flit & Setuptools as other dependency managers
    https://peps.python.org/pep-0621/

#### GitHub
- Pull request templates/issue templates should have YAML front matter
- Issue templates should be in the .github folder

#### Sketchy Ideas
- Has git tags for versions?
  - Versions in project files match latest git tag
    - Might need thought for cases where the version has been bumped but the tag hasn't been pushed yet
- Integrate with GitHub?

## Rules
| ID | Severity | Enabled for Project Types | Description | Advice |
|----|----------|---------------------------|-------------|--------|
| CI001 | Severity.MEDIUM | open-source, inner-source, team, personal | Projects should define a CI/CD pipeline to ensure code builds and works correctly | Consider creating a CI/CD pipeine for this project using a tool like GitHub Actions. A typical CI/CD pipeline should:</br>- Lint the code</br>- Build the code</br>- Run all tests</br>- Deploy any built artifacts like NuGet packages/PyPI packages</br></br>If at any point a step fails it should block the build |
| CS002 | Severity.MEDIUM | open-source, inner-source, team | C# projects should have a linter configured | C# projects should have a comprehensive linter configured such as StyleCop |
| CT001 | Severity.MEDIUM | open-source | Projects should have a CONTRIBUTING.md file describing how to contribute to the project | Create a CONTRIBUTING.md file in the root of the project and add content to describe to other users how they can contribute to the project in the most helpful way |
| GH001 | Severity.LOW | open-source, inner-source | GitHub projects should have an issue template | To help users create issues that are useful for you an issue template is recommended.</br></br>Create a .github/issue_template.md file and fill it with a template for users to use when filing issues.</br>See https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates |
| GH002 | Severity.LOW | open-source, inner-source | GitHub projects should have a pull request template | To help users create pull requests that are useful for you a pull request template is recommended.</br></br>Create a .github/pull_request_template.md file and fill it with a template for users to use when filing pull requests</br>See https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository |
| GI001 | Severity.HIGH | open-source, inner-source, team, personal | Projects should be tracked in Git version control | All projects, even the smallest personal projects benefit from being tracked in Git as it provides branch management, backups and history to your project.</br></br>Run `git init` in this project to setup Git and then make a commit |
| GI002 | Severity.HIGH | open-source, inner-source, team, personal | Projects in Git should have a remote copy in origin | This project does not have a Git remote named 'origin' which suggests there is no backup copy of the project should it be lost.</br></br>Setup a Git repository on your favourite Git service (e.g. GitHub) and follow the instructions to add a remote to an existing project. The instructions will likely look like:</br></br>git remote add origin <your url></br>git push origin master |
| GI003 | Severity.HIGH | open-source, inner-source, team, personal | Projects in Git should switch from a 'master' branch to a 'main' branch | This project has a branch named 'master' however it is now recommended to use a branch named 'main' to avoid culturally inappropriate language.</br></br>You can switch your primary branch using:</br></br>git checkout master</br>git pull origin master</br>git switch -c main</br>git push origin main</br>git branch -d master</br>git push :master</br></br>You may also need to make changes in your remote to change the default branch |
| GI004 | Severity.LOW | open-source, inner-source, team, personal | Projects in Git should have a .gitignore file | .gitignore files help you avoid committing unwanted files into Git such as binaries or build artifacts. You should create a .gitignore file for this project.</br></br>You can find comprehensive examples for your chosen language here https://github.com/github/gitignore |
| GI005 | Severity.LOW | open-source, inner-source, team, personal | Avoid committing .DS_store files | .DS_store files are OSX metadata files in a proprietary binary format. When committed to Git repositories they cause unnecessary changes and provide no value as they differ per machine.</br></br>You can tell git to ignore them from commits by adding them to your .gitignore.</br></br>You can also all them to your global .gitignore to avoid ever committing them in any repository. Configure a global .gitignore using the following:</br>git config --global core.excludesfile ~/.gitignore</br></br>To remove one from the current repository you can use:</br>git rm --cached ./path/to/.DS_Store |
| LI001 | Severity.MEDIUM | open-source, personal | Projects should have a LICENSE.md file describing how the project can be used | Create a LICENSE.md file in the root of the project and add content to describe to other users how this project can be used</br></br>If you are not familiar with the different licenses available to you, try https://choosealicense.com which guides you through the choice. |
| PY001 | Severity.MEDIUM | open-source, inner-source, team, personal | Python projects should prefer a build system to a requirements.txt | Python is moving towards using more intelligent build systems like Poetry or pipenv to manage dependencies. Consider switching from a requirements.txt file to one of these tools. |
| PY002 | Severity.MEDIUM | open-source, inner-source, team | Python projects should have a linter configured | Python projects should have a comprehensive linter configured such as Pylama |
| PY003 | Severity.MEDIUM | open-source, inner-source, team, personal | Python projects should prefer a build system to setup.py/setup.cfg | Python is moving towards using more intelligent build systems like Poetry or pipenv to manage dependencies. Consider switching from a setup.py or setup.cfg file to one of these tools. |
| RE001 | Severity.HIGH | open-source, inner-source, team, personal | Projects should have a README.md file describing the project and its use | Create a README.md file in the root of the project and add content to describe to other users (or just your future self) things like:</br>- Why does this project exist?</br>- How do I install it?</br>- How do I use it?</br>- What configuration can be set?</br>- How do I build the source code? |
| RE002 | Severity.LOW | open-source, inner-source, team, personal | README.md should contain an Installation section | To help users (and your future self) install your project/library you should provide an installation section in your README. Add the following to your readme:</br></br>## Installation</br>1. Do this</br>2. Now do this |
| RE003 | Severity.LOW | open-source, inner-source, team, personal | README.md should contain a Usage section | To help users (and your future self) use your project/library you should provide a usage section in your README. Add the following to your readme:</br></br>## Usage</br>To do this thing:</br>1. Do this</br>2. Then run this |
