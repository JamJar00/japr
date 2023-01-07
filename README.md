# Jamie's Awesome Project Rater
A cross-language tool for rating the overall quality of open source, commercial and personal projects

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
