from dataclasses import dataclass
from typing import TextIO
from collections import deque
from enum import Enum


TimeStamp = int


Identifier = int


class Direction(Enum):
    RIGHT = 1
    LEFT = -1

    def __int__(self):
        return self.value

@dataclass
class Package:
    identifier: Identifier
    arrival: TimeStamp
    source: int
    destination: int
    weight: int
    value: int


class Station:
    packages: deque[Package]

    ...


class Wagon:
    pos: int
    packages: dict[Identifier, Package]
    num_stations: int
    capacity: int
    current_load: int

    def __init__(self, num_stations: int, capacity: int) -> None: ...

    def move(self, direction: Direction) -> None: ...

    def load_package(self, p: Package) -> None: ...

    def deliver(self, identifier: Identifier) -> int: ...


class FullfilmentCenter:
    ...

    def __init__(self, num_stations: int, wagon_capacity: int) -> None: ...

    def cash(self) -> int: ...

    def wagon(self) -> Wagon: ...

    def num_stations(self) -> int: ...

    def station(self, idx: int) -> Station: ...

    def receive_package(self, p: Package) -> None: ...

    def deliver_package(self, identifier: Identifier) -> None: ...

    def current_station_package(self) -> Package | None: ...

    def load_current_station_package(self) -> None: ...


class Logger:
    """Class to log fcenter actions to a file."""

    _file: TextIO

    def __init__(self, path: str, name: str, num_stations: int, wagon_capacity: int) -> None:
        self._file = open(path, 'w')
        print(0, 'START', name, num_stations, wagon_capacity, file=self._file)

    def load(self, t: TimeStamp, identifier: Identifier) -> None:
        print(t, 'LOAD', identifier, file=self._file)

    def deliver(self, t: TimeStamp, identifier: Identifier) -> None:
        print(t, 'DELIVER', identifier, file=self._file)

    def move(self, t: TimeStamp, direction: Direction) -> None:
        print(t, 'MOVE', direction, file=self._file)

    def add(self, t: TimeStamp, identifier: Identifier) -> None:
        print(t, 'ADD', identifier, file=self._file)


def read_packages(path: str) -> list[Package]:
    """Returns a list of packages read from a file at path."""

    with open(path, 'r') as file:
        packages: list[Package] = []
        for line in file:
            identifier, arrival, location, destination, weight, value = map(int, line.split())
            package = Package(identifier, arrival, location, destination, weight, value)
            packages.append(package)
        return packages


def check_and_show(packages_path: str, log_path: str) -> None:
    """
    Check that the actions stored in the log at log_path with the packages at packages_path are legal.
    Raise an exception if not.
    // In the case that stdscr is not None, the store is written after each action.
    """

    # get the data
    packages = read_packages(packages_path)
    packages_map = {p.identifier: p for p in packages}
    log = open(log_path, 'r')
    lines = log.readlines()

    # process first line
    tokens = lines[0].split()
    assert len(tokens) == 5
    assert tokens[0] == "0"
    assert tokens[1] == "START"
    name = tokens[2]
    num_stations = int(tokens[3])
    wagon_capacity = int(tokens[4])
    fcenter = FullfilmentCenter(num_stations, wagon_capacity)
    last_wagon_action = -1
    last_package_arrival = -1

    for line in lines[1:]:
        tokens = line.split()
        t: TimeStamp = int(tokens[0])
        what = tokens[1]
        assert t >= max(last_wagon_action, last_package_arrival)

        p: Package | None = None

        if what == "ADD":
            assert t > last_wagon_action
            identifier = int(tokens[2])
            assert identifier in packages_map.keys()
            p = packages_map[identifier]
            assert p.arrival == t
            fcenter.receive_package(p)
            last_package_arrival = t
        elif what == "DELIVER":
            identifier = int(tokens[2])
            matches = list(filter(lambda p: p.identifier == identifier, fcenter.wagon().packages.values()))
            assert len(matches) == 1
            p = matches[0]
            fcenter.deliver_package(identifier)
            last_wagon_action = t
        elif what == "MOVE":
            direction = Direction(int(tokens[2]))
            fcenter.wagon().move(direction)
            last_wagon_action = t
        elif what == "LOAD":
            identifier = int(tokens[2])
            p = fcenter.current_station_package()
            assert p is not None
            assert p.identifier == identifier
            fcenter.load_current_station_package()
            assert 0 <= sum(pkg.weight for pkg in fcenter.wagon().packages.values()) <= wagon_capacity
            last_wagon_action = t
        else:
            assert False
