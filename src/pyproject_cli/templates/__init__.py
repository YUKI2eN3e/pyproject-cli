import re

import tomllib


def _get_min_python_version(pyproject_file: str) -> str:
    with open(pyproject_file, "rb") as file:
        pyproject = tomllib.load(file)

    python_version_str = pyproject["tool"]["poetry"]["dependencies"]["python"]
    python_version = re.sub(r"\D", "", python_version_str.split(",")[0])
    return f"py{python_version}"
