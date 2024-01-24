#!/usr/bin/env python3
from pyproject_cli import cli


def main():
    args = cli.get_args()
    print(args)


if __name__ == "__main__":
    main()
