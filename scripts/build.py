import argparse
import subprocess
import utils

from pathlib import Path


def generate(build_dir: Path, generator: str = ''):
    print(f'Generating {generator} project'.replace('  ', ' ') + '...')
    command = ['cmake']
    command += ['-D', 'JUCEY_CATCH2_FETCH_CATCH2=ON']
    command += ['-D', 'JUCEY_CATCH2_FETCH_JUCE=ON']
    command += ['-D', 'JUCEY_CATCH2_ADD_TEST_TARGETS=ON']
    command += ['-B', f'{build_dir}']

    if generator != '':
        command += ['-G', generator]

    subprocess.check_call(command)


def build(build_dir: Path, config: str):
    print(f'Building {config} targets...')
    command = ['cmake']
    command += ['--build', f'{build_dir}']
    command += ['--config', config]
    command += ['--parallel 8']
    subprocess.check_call(command)


def run_tests(tests_dir: Path, config: str):
    print(f'Running test targets...')
    command = ['ctest']
    command += ['-j', '64']
    command += ['-T', 'Test']
    command += ['-C', config]
    command += ['--test-dir', f'{tests_dir}']
    command.append('--stop-on-failure')
    command.append('--no-label-summary')
    command.append('--no-compress-output')
    command.append('--force-new-ctest-process')
    subprocess.check_call(command)


def main():
    with utils.git_repo_as_working_dir():
        default_build_dir = 'build'
        configs = ['Debug', 'Release']
        default_config = 'Release'

        parser = argparse.ArgumentParser()
        parser.add_argument('--build-dir', type=Path,
                            default=default_build_dir)
        parser.add_argument(
            '--config', default=default_config, choices=configs)

        generate_group = parser.add_mutually_exclusive_group()
        generate_group.add_argument(
            '--generate', type=str, const='', nargs='?')
        generate_group.add_argument(
            '--regenerate', type=str, const='', nargs='?')

        parser.add_argument('--build', action='store_true')
        parser.add_argument('--run-tests', action='store_true')

        args = parser.parse_args()

        if args.regenerate is not None:
            utils.remove_dir(args.build_dir)
            generate(build_dir=args.build_dir,
                     generator=args.regenerate)

        if args.generate is not None:
            generate(build_dir=args.build_dir,
                     generator=args.generate)

        if args.build:
            build(build_dir=args.build_dir,
                  config=args.config)

        if args.run_tests:
            run_tests(tests_dir=args.build_dir / 'tests',
                      config=args.config)


if __name__ == '__main__':
    main()
