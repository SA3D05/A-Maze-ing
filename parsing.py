from sys import argv


try:

    if len(argv) < 2:
        raise Exception("Missing 'config.txt'")
    elif len(argv) > 2:
        raise Exception("Too many arguments")
    filename: str = argv[1]
    if filename != "config.txt":
        raise Exception("Only accept 'config.txt'")

    i = 1
    lines: list[str] = list()
    info = dict()

    with open(argv[1]) as file:
        lines = [line for line in file]

    for line in lines:

        if line.startswith("#"):
            continue

        if "=" not in line:
            raise ValueError(f"invalid line '{line}'")

        if line.startswith("WIDTH"):

            print(line)


except Exception as e:
    print(f"Error: {e}")
