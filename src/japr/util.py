import os

# List of directories to immediately stop searching when looking for files
# This is designed to be a short and non-comprehensive list mostly in the interest of search speed
SKIP_DIRECTORIES = [
    # You know why this is skipped...
    "node_modules",
    # Stores git history as lots and lots of files we don't want to parse through
    ".git"
]

def _walk(base_path):
    with os.scandir(base_path) as scan:
        for obj in scan:
            if obj.is_dir() and obj.name not in SKIP_DIRECTORIES:
                yield from _walk(obj.path)
            elif obj.is_file():
                yield (obj.name, obj.path)


def find_files_with_extension(base_path, extension):
    yield from (obj_path for obj_name, obj_path in _walk(base_path) if obj_name.endswith(extension))


def find_files_with_name(base_path, name):
    yield from (obj_path for obj_name, obj_path in _walk(base_path) if obj_name == name)
