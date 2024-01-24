from typing import List

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

from pyproject_cli.templates import _get_min_python_version


def add_black_settings(pyproject_file: str) -> None:
    env = Environment(loader=FileSystemLoader("."))
    black_template = env.get_template("black.toml.js")

    pyproject: List[str]
    with open(pyproject_file, "r", encoding="utf8") as file:
        pyproject = file.readlines()

    with open(pyproject_file, "w", encoding="utf8") as file:
        file.writelines(pyproject)
        file.write(
            black_template.render(pyVersion=_get_min_python_version(pyproject_file))
        )
