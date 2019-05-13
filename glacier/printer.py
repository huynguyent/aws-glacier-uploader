from sys import stderr

from blessings import Terminal

term = Terminal()


def info(message):
    print(f"{term.bold_green('◦')} {message}", file=stderr)


def success(message):
    print(f"{term.green(message)}", file=stderr)


def error(message):
    print(f"{term.red(message)}", file=stderr)


def fatal(message, exit_code=1):
    error(message)
    exit(exit_code)