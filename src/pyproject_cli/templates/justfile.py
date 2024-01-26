import re
import subprocess
from os import path
from sys import platform

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


def get_windows_shell(git_path: str | None = None) -> str | None:
    if git_path is None:
        git_path = get_git_path()
        if git_path is None:
            return None
    if path.exists(path.join(git_path, DEFAULT_SHELL)):
        return (
            f'["{path.join(git_path, DEFAULT_SHELL)}", "-c"]'.replace("\\", "\\\\")
            if git_path is not None
            else None
        )
    else:
        try:
            git_path = path.dirname(git_path.removesuffix(path.sep))
            if path.exists(path.join(git_path, DEFAULT_SHELL)):
                return get_windows_shell(git_path)
            elif path.exists(path.join(git_path, "bin", DEFAULT_SHELL)):
                return get_windows_shell(git_path=path.join(git_path, "bin"))
            else:
                return get_windows_shell(git_path)
        except IndexError:
            return None


def write_justfile(
    justfile_path: str,
    pre_commit: bool = False,
    ipython: bool = False,
    black: bool = False,
    isort: bool = False,
    ruff: bool = False,
    mypy: bool = False,
    rich_argparse: bool = False,
    pyside6: bool = False,
    ui_src_path: str | None = None,
    ui_py_path: str | None = None,
) -> None:
    env = Environment(loader=FileSystemLoader(path.dirname(__file__)))
    justfile_template = env.get_template("justfile.j2")
    windows_shell = get_windows_shell() if platform == "win32" else None
    if windows_shell is None:
        windows_shell = path.join(DEFAULT_PATH, DEFAULT_SHELL)

    with open(justfile_path, "w", encoding="utf8") as file:
        file.write(
            justfile_template.render(
                {
                    "windows_shell": windows_shell,
                    "pre_commit": pre_commit,
                    "ipython": ipython,
                    "black": black,
                    "isort": isort,
                    "ruff": ruff,
                    "mypy": mypy,
                    "rich_argparse": rich_argparse,
                    "pyside6": pyside6,
                    "ui_src_path": ui_src_path,
                    "ui_py_path": ui_py_path,
                }
            )
        )
