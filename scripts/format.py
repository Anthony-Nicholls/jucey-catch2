import subprocess

from pathlib import Path


def git_filenames(working_dir: Path):
    return subprocess.run(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
        cwd=working_dir.resolve(),
        capture_output=True,
        check=True,
        universal_newlines=True).stdout.splitlines()


def is_cpp_file(file: Path):
    return file.suffix in ['.h', '.hpp', '.c', '.cpp']


def is_cmake_file(file: Path):
    return file.name == 'CMakeLists.txt' or file.suffix == '.cmake'


def is_python_file(file: Path):
    return file.suffix == '.py'


def apply_clang_format(file: Path):
    print(f'-- applying clang-format to {file.resolve()}')
    subprocess.run(['clang-format', '-i', file.resolve()], check=True)


def apply_cmake_format(file: Path):
    print(f'-- applying cmake-format to {file.resolve()}')
    subprocess.run(['cmake-format', '-i', file.resolve()], check=True)


def apply_autopep8(file: Path):
    print(f'-- applying autopep8 to {file.resolve()}')
    subprocess.run(['autopep8', '-a', '-a', '-i', file.resolve()], check=True)


def main():
    parent_dir = Path(__file__).parent.parent

    for filename in git_filenames(parent_dir):
        file_path = parent_dir / filename

        if is_cpp_file(file_path):
            apply_clang_format(file_path)

        if is_cmake_file(file_path):
            apply_cmake_format(file_path)

        if is_python_file(file_path):
            apply_autopep8(file_path)


if __name__ == '__main__':
    main()
