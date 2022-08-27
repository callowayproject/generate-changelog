"""The setup script."""

from pathlib import Path

from setuptools import setup


def parse_reqs(filepath: str) -> list:
    """
    Parse a file path containing requirements and return a list of requirements.

    Will properly follow ``-r`` and ``--requirements`` links like ``pip``. This
    means nested requirements will be returned as one list.

    Other ``pip``-specific lines are excluded.

    Args:
        filepath: The path to the requirements file

    Returns:
        All the requirements as a list.
    """
    path = Path(filepath)
    reqstr = path.read_text()
    reqs = []
    for line in reqstr.splitlines():
        line = line.strip()
        if line == "":
            continue
        elif not line or line.startswith("#"):
            # comments are lines that start with # only
            continue
        elif line.startswith("-r") or line.startswith("--requirement"):
            _, new_filename = line.split()
            new_file_path = path.parent / new_filename
            reqs.extend(parse_reqs(str(new_file_path)))
        elif line.startswith("-f") or line.startswith("-i") or line.startswith("--"):
            continue
        elif line.startswith("-Z") or line.startswith("--always-unzip"):
            continue
        else:
            reqs.append(line)
    return reqs


requirements = parse_reqs("requirements.txt")
dev_requirements = parse_reqs("requirements/dev.txt")
test_requirements = parse_reqs("requirements/test.txt")

setup(
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require={
        "dev": dev_requirements,
        "test": test_requirements,
    },
)
