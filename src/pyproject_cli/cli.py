from argparse import ArgumentParser
from dataclasses import dataclass
from os import path
from sys import argv
from typing import List

from argcomplete import autocomplete
from rich_argparse import HelpPreviewAction, RichHelpFormatter


@dataclass
class CliArgs:
    script_name: str
    script_string: str
    packages: List[str]

    rich_argparse: bool

    ruff: bool
    black: bool
    isort: bool
    pre_commit: bool
    ipython: bool


def get_args() -> CliArgs:
    module_name = path.basename(path.dirname(__file__))
    prog_name = module_name.replace("_", "-")

    parser = ArgumentParser(prog=prog_name, formatter_class=RichHelpFormatter)

    poetry_settings = parser.add_argument_group("Poetry Settings")
    poetry_settings.add_argument(
        "-N",
        "--script-name",
        dest="script_name",
        help="the name of the script in the `tool.poetry.scripts` section of `pyproject.toml`",
    )
    poetry_settings.add_argument(
        "-S",
        "--script-string",
        dest="script_string",
        help="the entrypoint string of the script in the `tool.poetry.scripts` section of `pyproject.toml`",
    )
    poetry_settings.add_argument(
        "-P",
        "--packages",
        dest="packages",
        nargs="+",
        help="the packages included in `pyproject.toml`",
    )

    enable_tools = parser.add_argument_group("Enable tools")
    enable_tools.add_argument(
        "--ruff", dest="ruff", action="store_true", default=False, help="enable `ruff`"
    )
    enable_tools.add_argument(
        "--black",
        dest="black",
        action="store_true",
        default=False,
        help="enable `black` (unnecessary if using `ruff`)",
    )
    enable_tools.add_argument(
        "--isort",
        dest="isort",
        action="store_true",
        default=False,
        help="enable `isort` (unnecessary if using `ruff`)",
    )
    enable_tools.add_argument(
        "--pre-commit",
        dest="pre_commit",
        action="store_true",
        default=False,
        help="pre-commit is installed in the pyproject",
    )
    enable_tools.add_argument(
        "--ipython",
        dest="ipython",
        action="store_true",
        default=False,
        help="ipython is installed in the pyproject",
    )

    if "--make-help-preview" in argv:
        parser.add_argument(
            "--make-help-preview",
            action=HelpPreviewAction,
            path=f".{path.sep}img{path.sep}help.svg",
        )

    autocomplete(parser)

    return CliArgs(**vars(parser.parse_args()))
