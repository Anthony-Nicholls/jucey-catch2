import os
import shutil
import subprocess
import sys
import time

from contextlib import contextmanager
from pathlib import Path


class Colour:
    OK = '\033[92m'
    FAIL = '\033[91m'
    CLEAR = '\033[0m'


def with_colour(colour: Colour, text: str):
    if sys.stdout.isatty():
        return f'{colour}{text}{Colour.CLEAR}'

    return text


def exit(message: str):
    if message:
        exit(with_colour(Colour.FAIL, message))
    exit()


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
        capture_output=True,
        check=True,
        universal_newlines=True).stdout.splitlines()

    deleted_git_files = subprocess.run(
        ['git', 'ls-files', '--deleted'],
        capture_output=True,
        check=True,
        universal_newlines=True).stdout.splitlines()

    return [Path(file) for file in git_files if file not in deleted_git_files]


@contextmanager
def status(message):
    print(f'-- {message}')
    start_time = time.perf_counter()
    try:
        yield
    except BaseException:
        print(with_colour(Colour.FAIL, f'-- {message} - failed'))
    else:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(with_colour(
            Colour.OK, f'-- {message} - done ({elapsed_time:.2f} sec)'))


def is_cpp_file(file: Path):
    return file.suffix in ['.h', '.hpp', '.c', '.cpp']


def is_cmake_file(file: Path):
    return file.name == 'CMakeLists.txt' or file.suffix == '.cmake'


def is_python_file(file: Path):
    return file.suffix == '.py'


def remove_dir(dir: Path):
    with status(f'Removing directory: {os.path.relpath(str(dir))}'):
        try:
            shutil.rmtree(dir)
        except FileNotFoundError:
            pass
