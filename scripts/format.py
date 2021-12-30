import os
import subprocess

from pathlib import Path

def git_filenames(working_dir: Path):
    return subprocess.run(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
        cwd=working_dir.resolve(), 
        capture_output=True,
        universal_newlines=True).stdout.splitlines()


def is_cpp_file(file: Path):
    return file.suffix in ['.h', '.hpp', '.c', '.cpp']


def is_cmake_file(file: Path):
    return file.name == 'CMakeLists.txt' or file.suffix == '.cmake'


def apply_clang_format(file: Path):
    print(f'-- applying clang-format to {file.resolve()}')
    subprocess.run(['clang-format', '-i', file.resolve()])


def apply_cmake_format(file: Path):
    print(f'-- applying cmake-format to {file.resolve()}')
    subprocess.run(['cmake-format', '-i', file.resolve()])


if __name__ == '__main__':
    parent_dir = Path(__file__).parent.parent

    for filename in git_filenames(parent_dir):
        file = parent_dir / filename

        if is_cpp_file(file):
            apply_clang_format(file)

        if is_cmake_file(file):
            apply_cmake_format(file)
