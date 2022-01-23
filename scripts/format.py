import argparse
import subprocess
import utils

from pathlib import Path


def apply_cpp_formatting(file: Path):
    with utils.status(f'Applying clang-format: {file}'):
        subprocess.check_call(['clang-format', '-i', file])


def apply_cmake_formatting(file: Path):
    with utils.status(f'Applying cmake-format: {file}'):
        subprocess.check_call(['cmake-format', '-i', file])


def apply_python_formatting(file: Path):
    with utils.status(f'Applying autopep8: {file}'):
        subprocess.check_call(['autopep8', '-i', file])


def apply_formatting_to_file(file: Path):
    if utils.is_cpp_file(file):
        apply_cpp_formatting(file)

    if utils.is_cmake_file(file):
        apply_cmake_formatting(file)

    if utils.is_python_file(file):
        apply_python_formatting(file)


def apply_formatting_to_files(files):
    for file in files:
        apply_formatting_to_file(file)


def cpp_file_needs_formatting(file: Path):
    with utils.status(f'Running clang-format checks: {file}'):
        subprocess.check_call(['clang-format', '--dry-run', '--Werror', file])
        return False
    return True


def cmake_file_needs_formatting(file: Path):
    with utils.status(f'Running cmake-format checks: {file}'):
        subprocess.check_call(['cmake-format', '--check', file])
        return False
    return True


def python_file_needs_formatting(file: Path):
    with utils.status(f'Running autopep8 checks: {file}'):
        subprocess.check_call(
            ['autopep8', '--exit-code', file], stdout=subprocess.PIPE)
        return False
    return True


def file_needs_formatting(file: Path):
    if utils.is_cpp_file(file):
        return cpp_file_needs_formatting(file)

    if utils.is_cmake_file(file):
        return cmake_file_needs_formatting(file)

    if utils.is_python_file(file):
        return python_file_needs_formatting(file)


def any_files_need_formatting(files):
    return any([file_needs_formatting(file) for file in files])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')

    args = parser.parse_args()

    with utils.git_repo_as_working_dir():
        if args.check:
            if any_files_need_formatting(utils.list_git_files()):
                utils.exit('error: files need formatting')
        else:
            apply_formatting_to_files(utils.list_git_files())
