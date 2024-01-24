import re
import subprocess
from os import path

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

DEFAULT_PATH = "C:\\Program Files\\Git\\"
DEFAULT_SHELL = "sh.exe"


def get_git_path() -> str | None:
    result = subprocess.run(["where", "git"], shell=True, capture_output=True)
    if result.returncode == 0:
        path_match = re.match(r"^[A-Z]:\\.*\\(?!git\.exe$)", result.stdout.decode())
        return (
            path_match[0].removesuffix(
                f"{path.basename(path.dirname(path_match[0]))}\\"
            )
            if path_match is not None
            else (DEFAULT_PATH if path.exists(DEFAULT_PATH) else None)
        )
    else:
        if path.exists(DEFAULT_PATH):
            return DEFAULT_PATH
    return None


def windows_shell(git_path: str | None = None) -> str | None:
    if git_path is None:
        git_path = get_git_path()
        return (
            f'["{path.join(git_path, DEFAULT_SHELL)}", "-c"]'.replace("\\", "\\\\")
            if git_path is not None
            else None
        )
    return f'["{path.join(git_path, DEFAULT_SHELL)}", "-c"]'.replace("\\", "\\\\")


def write_justfile(
    justfile_path: str,
    pre_commit: bool = False,
    ipython: bool = False,
    black: bool = False,
    isort: bool = False,
    ruff: bool = False,
    mypy: bool = False,
    rich_argparse: bool = False,
) -> None:
    env = Environment(loader=FileSystemLoader("."))
    justfile_template = env.get_template("justfile.j2")

    with open(justfile_path, "w", encoding="utf8") as file:
        file.write(
            justfile_template.render(
                {
                    "pre_commit": pre_commit,
                    "ipython": ipython,
                    "black": black,
                    "isort": isort,
                    "ruff": ruff,
                    "mypy": mypy,
                    "rich_argparse": rich_argparse,
                }
            )
        )
