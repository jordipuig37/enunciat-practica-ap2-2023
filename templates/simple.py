# """
# Template file for simple.py module.
# """

import sys
import curses

from fcenter import *


class Strategy:
    ...

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None: ...

    def cash(self) -> int: ...

    def exec(self, packages: list[Package]) -> None: ...


def init_curses() -> None:
    """Initializes the curses library to get fancy colors and whatnots."""

    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, curses.COLOR_WHITE, i)


def execute_strategy(packages_path: str, log_path: str, num_stations: int, wagon_capacity: int) -> None:
    """Execute the strategy on an fcenter with num_stations stations reading packages from packages_path and logging to log_path."""

    packages = read_packages(packages_path)
    strategy = Strategy(num_stations, wagon_capacity, log_path)
    strategy.exec(packages)


def main(stdscr: curses.window) -> None:
    """main script"""

    init_curses()

    packages_path = sys.argv[1]
    log_path = sys.argv[2]
    num_stations = int(sys.argv[3])
    wagon_capacity = int(sys.argv[4])

    execute_strategy(packages_path, log_path, num_stations, wagon_capacity)
    check_and_show(packages_path, log_path, stdscr)


if __name__ == '__main__':
    curses.wrapper(main)
