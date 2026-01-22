from sys import stderr


def pdeb(info: str):
    stderr.write(f"{info}\n")
