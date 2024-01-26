#!/usr/bin/env python3
from rich.console import Console

from pyproject_cli import cli, utils

console = Console()


def main():
    if not utils.pyproject_toml_exists():
        console.print(
            "[bold][red]Run `poetry init` then rerun this program.[/red][/bold]"
        )
    args = cli.get_args()
    if args.pre_commit and not utils.git_initialized():
        console.print("[bold][red]Run `git init` then rerun this program.[/red][/bold]")


if __name__ == "__main__":
    main()
