# """
# Template file for expert.py module.
# """

import sys

from fcenter import *


class Strategy:
    ...

    def __init__(self, num_stations: int, wagon_capacity: int, log_path: str) -> None: ...

    def cash(self) -> int: ...

    def exec(self, packages: list[Package]) -> None: ...


def execute_strategy(packages_path: str, log_path: str, num_stations: int, wagon_capacity: int) -> None:
    """Execute the strategy on an fcenter with num_stations stations reading packages from packages_path and logging to log_path."""

    packages = read_packages(packages_path)
    strategy = Strategy(num_stations, wagon_capacity, log_path)
    strategy.exec(packages)


def main() -> None:
    """main script"""

    packages_path = sys.argv[1]
    log_path = sys.argv[2]
    num_stations = int(sys.argv[3])
    wagon_capacity = int(sys.argv[4])

    execute_strategy(packages_path, log_path, num_stations, wagon_capacity)
    check_and_show(packages_path, log_path)


if __name__ == '__main__':
    main()
