import subprocess


def install_dependency(dependency: str):
    subprocess.run(['pip3', 'install', dependency])


def main():
    install_dependency('cmake')
    install_dependency('cmakelang')
    install_dependency('clang-format')
    install_dependency('autopep8')


if __name__ == '__main__':
    main()
