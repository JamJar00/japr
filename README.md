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

## TODO
### Checks
- Check lock files are checked into Git
- No TODOs anywhere, they should be tracked in issues
- More languages

#### Python
- Avoid setup.py/setup.cfg in favour of pyproject.toml?

#### Sketchy Ideas
- Has link in readme to Docker Hub if it has a Docker artifact
- Has git tags for versions?
  - Versions in project files match latest git tag
- Integrate with GitHub?

## Rules
| ID | Severity | Enabled for Project Types | Description | Advice |
|----|----------|---------------------------|-------------|--------|
| CI001 | Severity.MEDIUM | open-source, inner-source, team, personal | Projects should define a CI/CD pipeline to ensure code builds and works correctly | Consider creating a CI/CD pipeine for this project using a tool like GitHub Actions. A typical CI/CD pipeline should:</br>- Lint the code</br>- Build the code</br>- Run all tests</br>- Deploy any built artifacts like NuGet packages/PyPI packages</br></br>If at any point a step fails it should block the build |
| CS003 | Severity.MEDIUM | open-source, inner-source, team | C# projects should have a linter configured | C# projects should have a comprehensive linter configured such as StyleCop |
| GH001 | Severity.LOW | open-source, inner-source | GitHub projects should have an issue template | To help users create issues that are useful for you an issue template is recommended.</br></br>Create a .github/ISSUE_TEMPLATE.md file and fill it with a tempate for users to use when filing issues |
| GH002 | Severity.LOW | open-source, inner-source | GitHub projects should have a pull request template | To help users create pull requests that are useful for you a pull request template is recommended.</br></br>Create a .github/PULL_REQUEST_TEMPLATE.md file and fill it with a tempate for users to use when filing pull requests |
| GI001 | Severity.HIGH | open-source, inner-source, team, personal | Projects should be tracked in Git version control | All projects, even the smallest personal projects benefit from being tracked in Git as it provides branch management, backups and history to your project.</br></br>Run `git init` in this project to setup Git and then make a commit |
| GI002 | Severity.HIGH | open-source, inner-source, team, personal | Projects in Git should have a remote copy in origin | This project does not have a Git remote named 'origin' which suggests there is no backup copy of the project should it be lost.</br></br>Setup a Git repository on your favourite Git service (e.g. GitHub) and follow the instructions to add a remote to an existing project. The instructions will likely look like:</br></br>git remote add origin <your url></br>git push origin master |
| GI003 | Severity.HIGH | open-source, inner-source, team, personal | Projects in Git should switch from a 'master' branch to a 'main' branch | This project has a branch named 'master' however it is now recommended to use a branch named 'main' to avoid culturally inappropriate language.</br></br>You can switch your primary branch using:</br></br>git checkout master</br>git pull origin master</br>git switch -c main</br>git push origin main</br>git branch -d master</br>git push :master</br></br>You may also need to make changes in your remote to change the default branch |
| GI004 | Severity.LOW | open-source, inner-source, team, personal | Projects in Git should have a .gitignore file | .gitignore files help you avoid committing unwanted files into Git such as binaries or build artifacts. You should create a .gitignore file for this project.</br></br>You can find comprehensive examples for your chosen language here https://github.com/github/gitignore |
| LI001 | Severity.MEDIUM | open-source, personal | Projects should have a LICENSE.md file describing how the project can be used | Create a LICENSE.md file in the root of the project and add content to describe to other users how this project can be used</br></br>If you are not familiar with the difference licenses available to you, try https://choosealicense.com which guides you through the choice. |
| PY001 | Severity.MEDIUM | open-source, inner-source, team, personal | Python projects should prefer a build system to a requirements.txt | Python is moving towards using more intelligent build systems like Poetry or pipenv to manage dependencies. Consider switching from a requirements.txt file to one of these tools. |
| PY002 | Severity.LOW | open-source, inner-source, team, personal | Python projects should have a dependency manager | Python projects should have some way of tracking dependencies for the project, such as a pyproject.toml with Poetry or a Pipfile, even if they have no dependencies.</br></br>Setup a tool like Poetry or pipenv. |
| PY003 | Severity.MEDIUM | open-source, inner-source, team | Python projects should have a linter configured | Python projects should have a comprehensive linter configured such as Pylama |
| RE001 | Severity.HIGH | open-source, inner-source, team, personal | Projects should have a README.md file describing the project and its use | Create a README.md file in the root of the project and add content to describe to other users (or just your future self) things like:</br>- Why does this project exist?</br>- How do I install it?</br>- How do I use it?</br>- What configuration can be set?</br>- How do I build the source code? |
| RE002 | Severity.LOW | open-source, inner-source, team, personal | README.md should contain an Installation section | To help users (and your future self) install your project/library you should provide an installation section in your README. Add the following to your readme:</br></br>## Installation</br>1. Do this</br>2. Now do this |
| RE003 | Severity.LOW | open-source, inner-source, team, personal | README.md should contain a Usage section | To help users (and your future self) use your project/library you should provide a usage section in your README. Add the following to your readme:</br></br>## Usage</br>To do this thing:</br>1. Do this</br>2. Then run this |
