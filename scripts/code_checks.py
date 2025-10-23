from west.commands import WestCommand
import subprocess
import os
from pathlib import Path

# Directories to exclude
EXCLUDED_DIRS = ['build']

def should_include(path):
    return not any(excluded in str(path) for excluded in EXCLUDED_DIRS)

def collect_files():
    project_path = Path('.')
    c_files = [str(p) for p in project_path.rglob('*.c') if should_include(p)]
    h_files = [str(p) for p in project_path.rglob('*.h') if should_include(p)]
    print(f'→ Found {len(c_files)} .c files and {len(h_files)} .h files.')
    return c_files + h_files

class Format(WestCommand):
    def __init__(self):
        super().__init__(
            'format',
            'Run clang-format on project files',
            'Applies clang-format to all .c and .h files (excluding build and objdict).'
        )

    def do_add_parser(self, parser_adder):
        return parser_adder.add_parser(self.name)

    def do_run(self, args, unknown_args):
        files = collect_files()
        print('→ Running clang-format...')
        subprocess.run(['clang-format', '-i', '-style=file'] + files, check=True)

class Cppcheck(WestCommand):
    def __init__(self):
        super().__init__(
            'cppcheck',
            'Run cppcheck static analysis',
            'Runs cppcheck on all .c and .h files with custom suppression rules.'
        )

    def do_add_parser(self, parser_adder):
        return parser_adder.add_parser(self.name)

    def do_run(self, args, unknown_args):
        files = collect_files()
        suppressions_file = 'cppcheck.supp'

        cppcheck_cmd = [
            'cppcheck',
            '-q', '--force', '--enable=all', '--error-exitcode=1',
            f'--suppressions-list={suppressions_file}',
            '--template={file}:{line}: {severity} ({id}): {message}'
        ] + files

        print('→ Running cppcheck...')
        subprocess.run(cppcheck_cmd, check=True)

