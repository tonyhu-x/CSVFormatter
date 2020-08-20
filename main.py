"""This is a CSV formatter."""

MAX_LINE_COUNT = 1024
MAX_LINE_WIDTH = 512


def read(file_name: str) -> list:
    """Read the contents of the file."""
    lst = list()

    with open(file_name, 'r') as f:
        for _ in range(MAX_LINE_COUNT):
            line = f.readline()
            if line == '':  # we have reached EOF
                break
            elif not line.strip():  # if line contains only whitespace
                continue
            if len(line) > MAX_LINE_WIDTH:
                raise RuntimeError('Line too long!')
            lst.append(line)
        if f.readline != '':
            raise RuntimeError('File contains too many lines')

    return lst

def format(lst: list):
    nlst = list()
    