import sys

import click


@click.command()
@click.argument("file", type=click.File("r"), required=False)
def nl_command(file):
    input_stream = file if file else sys.stdin

    line_number = 1
    for line in input_stream:
        print(f"{line_number:6d}\t{line}", end="")
        line_number += 1

if __name__ == "__main__":
    nl_command()
