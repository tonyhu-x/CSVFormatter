"""This is a CSV formatter."""

import argparse
import sys

from console.utils import wait_key

MAX_LINE_COUNT = 1024
MAX_LINE_WIDTH = 512
DEFAULT_DISPLAY_LINE_COUNT = 10


def read(file_name: str) -> list:
    """Read the contents of the file."""
    lst = list()
    col_count = -1

    with open(file_name, 'r') as f:
        try:
            for i in range(MAX_LINE_COUNT):
                line = f.readline()
                if line == '':  # we have reached EOF
                    break
                line = line.strip()
                if not line:  # if line contains only whitespace
                    continue
                if len(line) > MAX_LINE_WIDTH:
                    raise RuntimeError('Line too long!')
                temp_lst = line.split(',')
                temp_col_count = len(temp_lst)
                if col_count == -1:
                    col_count = temp_col_count
                elif col_count != temp_col_count:
                    raise RuntimeError(
                        f'Error in line {i + 1}: expected {col_count} column(s) but found {temp_col_count}')
                lst.append(temp_lst)
            if f.readline() != '':
                raise RuntimeError('File contains too many lines')
        except RuntimeError as e:
            print(str(e))
            exit(1)

    return lst


def print_formatted(contents: list, line_count: int):
    """Print the contents."""
    lengths = [-1] * len(contents[0])

    for i in range(len(lengths)):
        for j in contents:
            lengths[i] = max(len(j[i]), lengths[i])

    count = 0
    for ln in contents:
        if count == line_count:
            count = 0
            print('>', end='')
            wait_key()
            print()
        for i, tok in enumerate(ln):
            print(tok + ' ' * (lengths[i] - len(tok)), end='')
            if i != len(ln) - 1:
                print(',', end='')
        print()
        count += 1


def main(args: argparse.Namespace):
    """This is the main function."""
    contents = read(args.file_name)
    print_formatted(contents, args.lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A command line CSV viewer and formatter.')
    parser.add_argument('-l', '--lines', type=int, default=DEFAULT_DISPLAY_LINE_COUNT, help='specify the number of lines to display on each screen')
    parser.add_argument('file_name')
    args = parser.parse_args()
    main(args)  # remove the name argument
