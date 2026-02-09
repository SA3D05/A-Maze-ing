from typing import Tuple


class MazeConfig:
    def __init__(
        self,
    ) -> None:

        self.height: int = 10
        self.width: int = 10
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (9, 9)
        self.output: str = "output.txt"
        self.perfect: bool = False

    def parse_config(self, config_file: str):
        config_info = {}
        with open(config_file, "r") as fd:

            for line in fd:

                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    config_info[key.strip().upper()] = value.strip()

            self.width = int(config_info.get("WIDTH", 10))

            self.height = int(config_info.get("HEIGHT", 10))

            is_perfect_str = config_info.get("PERFECT", "TRUE").strip().upper()

            self.is_perfect = is_perfect_str == "TRUE"

            # self.entry = tuple([config_info.get("ENTRY", "0,0").split(",")])

            # self.exit = tuple([config_info.get("EXIT", "9,9").split(",")])
