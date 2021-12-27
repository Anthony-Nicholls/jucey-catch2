import argparse
import shutil
import subprocess

from pathlib import Path
from contextlib import contextmanager


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
            shutil.rmtree(build_dir)
        except FileNotFoundError:
            pass


def generate(generator_name: str = ''):
    with status(f'Generating {generator_name} project'.replace('  ', ' ')):
        args = ['cmake']
        args += ['-D', 'JUCEY_CATCH2_FETCH_CATCH2=ON']
        args += ['-D', 'JUCEY_CATCH2_FETCH_JUCE=ON']
        args += ['-D', 'JUCEY_CATCH2_ADD_TEST_TARGETS=ON']
        args += ['-B', build_dir]

        if generator_name != '':
            args += ['-G', generator_name]

        subprocess.call(args)


def build(config: str):
    with status(f'Building {config} targets'):
        args = ['cmake']
        args += ['--build', build_dir]
        args += ['--config', config]
        args += ['--parallel 8']
        subprocess.call(args)


def run_tests(config: str):
    with status(f'Running test targets'):
        args = ['ctest']
        args += ['-j', '64']
        args += ['-T', 'Test']
        args += ['-C', config]
        args += ['--test-dir', tests_dir]
        args.append('--stop-on-failure')
        args.append('--no-label-summary')
        args.append('--no-compress-output')
        args.append('--force-new-ctest-process')
        subprocess.call(args)


if __name__ == '__main__':
    build_dir = Path(__file__).parent.parent / 'build'
    tests_dir = build_dir / 'tests'

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
    group.add_argument('--run-tests',  action='store_true')

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
