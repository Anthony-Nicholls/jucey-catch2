import argparse
import subprocess
import utils

from pathlib import Path


def is_cpp_file(file: Path):
    return file.suffix in ['.h', '.hpp', '.c', '.cpp']


def is_cmake_file(file: Path):
    return file.name == 'CMakeLists.txt' or file.suffix == '.cmake'


def is_python_file(file: Path):
    return file.suffix == '.py'


def apply_cpp_formatting(file: Path):
    subprocess.run(['clang-format', '-i', str(file)], check=True)


def apply_cmake_formatting(file: Path):
    subprocess.run(['cmake-format', '-i', str(file)], check=True)


def apply_python_formatting(file: Path):
    subprocess.run(['autopep8', '-i', str(file)], check=True)


def apply_formatting_to_file(file: Path):
    if is_cpp_file(file):
        apply_cpp_formatting(file)

    if is_cmake_file(file):
        apply_cmake_formatting(file)

    if is_python_file(file):
        apply_python_formatting(file)


def cpp_file_needs_formatting(file: Path):
    command = ['clang-format', '--dry-run', '--Werror', str(file)]
    return subprocess.run(command).returncode != 0


def cmake_file_needs_formatting(file: Path):
    command = ['cmake-format', '--check', str(file)]
    return subprocess.run(command, capture_output=True).returncode != 0


def python_file_needs_formatting(file: Path):
    command = ['autopep8', '--exit-code', str(file)]
    return subprocess.run(command, capture_output=True).returncode != 0


def file_needs_formatting(file: Path):
    if is_cpp_file(file):
        return cpp_file_needs_formatting(file)

    if is_cmake_file(file):
        return cmake_file_needs_formatting(file)

    if is_python_file(file):
        return python_file_needs_formatting(file)

    return False


def is_formattable_file_type(file: Path):
    return any([is_cpp_file(file), is_cmake_file(file), is_python_file(file)])


def run_formatting_checks(files):
    num_failed = 0

    for file in files:
        if not is_formattable_file_type(file):
            print(utils.grey_text('no tests') + f' - {file}')

        elif file_needs_formatting(file):
            print(utils.red_text('failed') + f' - {file}')
            num_failed += 1

        else:
            print(utils.green_text('passed') + f' - {file}')

    exit(num_failed)


def apply_formatting_to_files(files):
    for file in utils.list_git_files():
        if is_formattable_file_type(file):
            print(f'formatting {file}')
            apply_formatting_to_file(file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')

    args = parser.parse_args()

    with utils.git_repo_as_working_dir():
        if args.check:
            run_formatting_checks(utils.list_git_files())
        else:
            apply_formatting_to_files(utils.list_git_files())


if __name__ == '__main__':
    main()
