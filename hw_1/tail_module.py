import sys

import click


def read_last_lines(file, num_lines=10):
    try:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return lines[-num_lines:] if len(lines) >= num_lines else lines
    except Exception as e:
        print(f"Ошибка при чтении файла {file}: {e}", file=sys.stderr)
        return []


def print_last_lines(file, num_lines=10, print_header=False):
    if print_header:
        print(f"==> {file} <==")

    lines = read_last_lines(file, num_lines)
    for line in lines:
        print(line, end="")


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def tail_command(files):
    if not files:
        stdin_lines = sys.stdin.readlines()
        for line in stdin_lines[-17:]:
            print(line, end="")
    else:
        for i, file in enumerate(files):
            print_header = len(files) > 1

            if i > 0 and print_header:
                print()

            print_last_lines(file, 10, print_header)


if __name__ == "__main__":
    tail_command()
