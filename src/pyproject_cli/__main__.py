#!/usr/bin/env python3
from rich.console import Console

from pyproject_cli import cli, utils
from pyproject_cli.templates import justfile

console = Console()


def main():
    if not utils.pyproject_toml_exists():
        console.print(
            "[bold][red]Run `poetry init` then rerun this program.[/red][/bold]"
        )
        exit(1)
    args = cli.get_args()
    if args.pre_commit and not utils.git_initialized():
        console.print("[bold][red]Run `git init` then rerun this program.[/red][/bold]")
        exit(1)

    if args.update_pyproject:
        from pyproject_cli.templates import pyproject

        pyproject.update_pyproject_settings(
            pyproject_file="pyproject.toml",
            packages=args.packages,
            script_name=args.script_name,
            script_string=args.script_string,
            isort=args.isort,
            black=args.black,
            ruff=args.ruff,
        )

    if args.pre_commit:
        from pyproject_cli.templates import pre_commit_config

        pre_commit_config.write_pre_commit_config(
            git_root_path=utils.DEFAULT_GIT_ROOT,
            isort=args.isort,
            black=args.black,
            ruff=args.ruff,
            mypy=args.mypy,
        )

    justfile.write_justfile(
        justfile_path="justfile",
        pre_commit=args.pre_commit,
        ipython=args.ipython,
        black=args.just_black,
        isort=args.just_isort,
        ruff=args.ruff,
        mypy=args.mypy,
        rich_argparse=args.rich_argparse,
        pyside6=args.pyside6,
        ui_src_path=args.ui_src_path,
        ui_py_path=args.ui_py_path,
    )


if __name__ == "__main__":
    main()
