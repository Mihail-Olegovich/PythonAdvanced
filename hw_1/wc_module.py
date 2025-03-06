import sys

import click


def count_stats(content):
    line_count = content.count("\n")
    word_count = len(content.split())
    byte_count = len(content.encode("utf-8"))
    return line_count, word_count, byte_count


def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        stats = count_stats(content)
        return stats
    except Exception as e:
        print(f"wc: {file_path}: {str(e)}", file=sys.stderr)
        return 0, 0, 0


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def wc_command(files):
    total_lines, total_words, total_bytes = 0, 0, 0

    if not files:
        content = sys.stdin.read()
        lines, words, bytes_count = count_stats(content)
        print(f"{lines:8} {words:8} {bytes_count:8}")
        return

    for file_path in files:
        lines, words, bytes_count = process_file(file_path)
        print(f"{lines:8} {words:8} {bytes_count:8} {file_path}")

        total_lines += lines
        total_words += words
        total_bytes += bytes_count

    if len(files) > 1:
        print(f"{total_lines:8} {total_words:8} {total_bytes:8} total")


if __name__ == "__main__":
    wc_command()
