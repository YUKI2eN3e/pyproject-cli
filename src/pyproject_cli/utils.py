from os import path

DEFAULT_PYPROJECT_TOML = path.join(".", "pyproject.toml")
DEFAULT_GIT_ROOT = path.join(".", ".git")


def pyproject_toml_exists() -> bool:
    return path.exists(DEFAULT_PYPROJECT_TOML)


def git_initialized() -> bool:
    return path.exists(DEFAULT_GIT_ROOT)
