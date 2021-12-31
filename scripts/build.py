import argparse
import shutil
import subprocess

from pathlib import Path
from contextlib import contextmanager

BUILD_DIR = Path(__file__).parent.parent / 'build'
TESTS_DIR = BUILD_DIR / 'tests'


@contextmanager
def status(message):
    print(f'-- {message}')
    try:
        yield
    finally:
        print(f'-- {message} - done')


def clean():
    with status('Cleaning build directory'):
        try:
            shutil.rmtree(BUILD_DIR)
        except FileNotFoundError:
            pass


def generate(generator_name: str = ''):
    with status(f'Generating {generator_name} project'.replace('  ', ' ')):
        command = ['cmake']
        command += ['-D', 'JUCEY_CATCH2_FETCH_CATCH2=ON']
        command += ['-D', 'JUCEY_CATCH2_FETCH_JUCE=ON']
        command += ['-D', 'JUCEY_CATCH2_ADD_TEST_TARGETS=ON']
        command += ['-B', BUILD_DIR]

        if generator_name != '':
            command += ['-G', generator_name]

        subprocess.run(command, check=True)


def build(config: str):
    with status(f'Building {config} targets'):
        command = ['cmake']
        command += ['--build', BUILD_DIR]
        command += ['--config', config]
        command += ['--parallel 8']
        subprocess.run(command, check=True)


def run_tests(config: str):
    with status('Running test targets'):
        command = ['ctest']
        command += ['-j', '64']
        command += ['-T', 'Test']
        command += ['-C', config]
        command += ['--test-dir', TESTS_DIR]
        command.append('--stop-on-failure')
        command.append('--no-label-summary')
        command.append('--no-compress-output')
        command.append('--force-new-ctest-process')
        subprocess.run(command, check=True)


def main():
    configs = ['Debug', 'Release']
    default_config = 'Release'

    parser = argparse.ArgumentParser()
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--config',
                        default=default_config,
                        choices=configs)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--generate', type=str, const='', nargs='?')
    group.add_argument('--build', action='store_true')
    group.add_argument('--run-tests', action='store_true')

    args = parser.parse_args()

    if args.clean:
        clean()

    if args.generate is not None:
        generate(args.generate)

    if args.build:
        generate()
        build(config=args.config)

    if args.run_tests:
        generate()
        build(config=args.config)
        run_tests(config=args.config)


if __name__ == '__main__':
    main()
