import os
import shutil
import subprocess
import sys

from contextlib import contextmanager
from pathlib import Path


def apply_colour_to_text(colour_code, text: str):
    if sys.stdout.isatty():
        return f'{colour_code}{text}\033[0m'

    return text


def green_text(text: str):
    return apply_colour_to_text('\033[92m', text)


def red_text(text: str):
    return apply_colour_to_text('\033[91m', text)


def grey_text(text: str):
    return apply_colour_to_text('\033[90m', text)


def git_repo_dir():
    script = Path(__file__)
    scripts_dir = script.parent
    return (scripts_dir.parent.resolve())


@contextmanager
def working_dir(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


def git_repo_as_working_dir():
    return working_dir(git_repo_dir())


def list_git_files():
    git_files = subprocess.run(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
        check=True,
        universal_newlines=True,
        capture_output=True).stdout.splitlines()

    deleted_git_files = subprocess.run(
        ['git', 'ls-files', '--deleted'],
        check=True,
        universal_newlines=True,
        capture_output=True).stdout.splitlines()

    return [Path(file) for file in git_files if file not in deleted_git_files]


def remove_dir(dir: Path):
    try:
        shutil.rmtree(dir)
    except FileNotFoundError:
        pass
