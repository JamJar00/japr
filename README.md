# Healthcheck
A health check for your projects

## Installation
TODO

## Usage
```bash
healthcheck <project> [--summary]
```

### Suppressing Checks
If you need to suppress a check (boooooo) then you can create a `healthcheck.yaml` file in the root of your project that looks something like this:
```yaml
override:
  - id: CI001
    ignore: true
```

## Supported Languages
Health Check will work for projects of all languages however there are additional checks for the following:
- Python

## TODO
### Fundamentals
- Find a way to add suppressions

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
