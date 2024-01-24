from os import path

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader


def write_pre_commit_config(
    git_root_path: str = ".",
    isort: bool = False,
    black: bool = False,
    ruff: bool = False,
    mypy: bool = False,
) -> None:
    env = Environment(loader=FileSystemLoader("."))
    pre_commit_config_template = env.get_template("pre-commit-config.yaml.j2")
    with open(
        path.join(git_root_path, ".pre-commit-config.yaml"), "w", encoding="utf8"
    ) as file:
        file.write(
            pre_commit_config_template.render(
                {"isort": isort, "black": black, "ruff": ruff, "mypy": mypy}
            )
        )
