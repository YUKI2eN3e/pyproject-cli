from os import path


def pyproject_toml_exists() -> bool:
    return path.exists(path.join(".", "pyproject.toml"))


def git_initialized() -> bool:
    return path.exists(path.join(".", ".git"))
