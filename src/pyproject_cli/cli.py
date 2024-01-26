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

    # packages that get used in justfile
    rich_argparse: bool
    pyside6: bool
    # paths for pyside6
    ui_src_path: str | None
    ui_py_path: str | None

    # Tools
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
    setting_script = (
        "-N" in argv
        or "--script-name" in argv
        or "-S" in argv
        or "--script-string" in argv
    )
    poetry_settings.add_argument(
        "-N",
        "--script-name",
        dest="script_name",
        required=setting_script,
        help="the name of the script in the `tool.poetry.scripts` section of `pyproject.toml`",
    )
    poetry_settings.add_argument(
        "-S",
        "--script-string",
        dest="script_string",
        required=setting_script,
        help="the entrypoint string of the script in the `tool.poetry.scripts` section of `pyproject.toml`",
    )
    poetry_settings.add_argument(
        "-P",
        "--packages",
        dest="packages",
        nargs="+",
        help="the packages included in `pyproject.toml`",
    )

    interactive_packages = parser.add_argument_group("Interactive Packages")
    interactive_packages.add_argument(
        "--rich-argparse",
        dest="rich_argparse",
        action="store_true",
        default=False,
        help="use if you are using rich-argparse with a `--make-help-preview` arg and what it called when building",
    )
    interactive_packages.add_argument(
        "--qt",
        "--pyside6",
        dest="pyside6",
        action="store_true",
        default=False,
        help="use if you are using PySide6 and want to compile your `.ui` files on run/build as well as launch Designer via `just`",
    )

    using_pyside6 = "--qt" in argv or "--pyside6" in argv
    ui_paths = parser.add_argument_group(
        title="UI Paths", description="Only required if using PySide6"
    )
    ui_paths.add_argument(
        "--ui-src",
        dest="ui_src_path",
        default=None,
        required=using_pyside6,
        help="the path to your `.ui` files",
    )
    ui_paths.add_argument(
        "--ui-py",
        "--ui-out",
        dest="ui_py_path",
        default=None,
        required=using_pyside6,
        help="the path where you want your compiled `.ui` files to be placed",
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
