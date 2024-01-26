# mypy: disable-error-code="index, union-attr"
from os import path
from typing import List, Literal

from tomlkit import dumps, load, table

from pyproject_cli.templates import _get_min_python_version


def _get_src_dir(package_path: str) -> str:
    if "/" in package_path:
        return path.dirname(package_path).removesuffix(path.basename(path.curdir))
    elif "\\" in package_path:
        package_path = package_path.replace("\\", "/")
        while "//" in package_path:
            package_path = package_path.replace("//", "/")
        return _get_src_dir(package_path)
    elif "." in package_path:
        package_path = package_path.replace(".", "/")
        while "//" in package_path:
            package_path = package_path.replace("//", "/")
        return _get_src_dir(package_path)
    raise ValueError(package_path)


def _get_package_name(package_path: str) -> str:
    if "/" in package_path:
        return package_path.split("/")[-1]
    elif "\\" in package_path:
        package_path = package_path.replace("\\", "/")
        while "//" in package_path:
            package_path = package_path.replace("//", "/")
        return _get_package_name(package_path)
    elif "." in package_path:
        package_path = package_path.replace(".", "/")
        while "//" in package_path:
            package_path = package_path.replace("//", "/")
        return _get_package_name(package_path)
    raise ValueError(package_path)


def update_pyproject_settings(
    pyproject_file: str,
    packages: List[str],
    script_name: str | None = None,
    script_string: str | None = None,
    isort: bool = False,
    black: bool = False,
    ruff: bool = False,
    pydocstyle: Literal["google", "numpy", "pep257"] = "google",
) -> None:
    with open(pyproject_file, "rb") as file:
        pyproject = load(file)

    if packages != []:
        pyproject["tool"]["poetry"]["packages"] = []
        for package in packages:
            pyproject["tool"]["poetry"]["packages"].append(  # type: ignore[call-arg]
                {  # type: ignore[arg-type]
                    "include": _get_package_name(package),
                    "from": _get_src_dir(package),
                }
            )

    if script_name is not None and script_string is not None:
        pyproject["tool"]["poetry"].add("scripts", table())
        pyproject["tool"]["poetry"]["scripts"][script_name] = script_string

    if isort:
        pyproject["tool"].add("isort", table())
        pyproject["tool"]["isort"]["profile"] = "black"
        pyproject["tool"]["isort"]["line_length"] = 88

    min_python: str | None = None

    if black:
        if min_python is None:
            min_python = _get_min_python_version(pyproject_file)
        pyproject["tool"].add("black", table())
        pyproject["tool"]["black"]["line-length"] = 88
        pyproject["tool"]["black"]["target-version"] = [min_python]
        pyproject["tool"]["black"]["include"] = r"\.pyi?$"

    if ruff:
        if min_python is None:
            min_python = _get_min_python_version(pyproject_file)
        pyproject["tool"].add("ruff", table())
        pyproject["tool"]["ruff"]["line-length"] = 88
        pyproject["tool"]["ruff"]["target-version"] = [min_python]
        pyproject["tool"]["ruff"]["extend-select"] = ["I"]
        pyproject["tool"]["ruff"]["ignore"] = ["E402"]

        pyproject["tool"]["ruff"].add("per-file-ignores", table())
        pyproject["tool"]["ruff"]["per-file-ignores"]["__init__.py"] = ["F401", "F403"]

        pyproject["tool"]["ruff"].add("isort", table())
        pyproject["tool"]["ruff"]["isort"]["case-sensitive"] = True

        pyproject["tool"]["ruff"].add("format", table())
        pyproject["tool"]["ruff"]["format"]["quote-style"] = "double"
        pyproject["tool"]["ruff"]["format"]["indent-style"] = "space"
        pyproject["tool"]["ruff"]["format"]["skip-magic-trailing-comma"] = False
        pyproject["tool"]["ruff"]["format"]["line-ending"] = "auto"

        pyproject["tool"]["ruff"].add("pydocstyle", table())
        pyproject["tool"]["ruff"]["pydocstyle"]["convention"] = pydocstyle

    with open(pyproject_file, "w", encoding="utf8") as file:
        lines = dumps(pyproject).splitlines()
        for line in lines:
            if "\\\\.pyi?$" in line:
                line = line.replace("\\\\", "\\").replace('"', "'")
            file.write(line + "\n")
