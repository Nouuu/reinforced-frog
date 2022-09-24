from conf.config import *


class World:
    def __init__(self, str_world: str, str_entities: str):
        self.__parse_world(str_world)
        self.__parse_entities(str_entities)
        self.__nb_world_states = len(self.__world_states)
        self.__nb_entities_states = len(self.__entities_states)

    def __parse_world(self, str_world):
        self.__world_states = {}
        row = 0
        col = 0
        for row, line in enumerate(str_world.strip().splitlines()):
            for col, char in enumerate(line):
                self.__world_states[(row, col)] = char

        self.__rows = int((row + 1) / 2)
        self.__cols = int((col + 1) / 2)

    def __parse_entities(self, str_entities):
        self.__entities_states = {}
        self.__goals = []
        row = 0
        col = 0
        for row, line in enumerate(str_entities.strip().splitlines()):
            for col, char in enumerate(line):
                if char == START_TOKEN:
                    self.__start = (row, col)
                elif char == EXIT_TOKEN:
                    self.__goals.append((row, col))
                self.__entities_states[(row, col)] = char

        if int((row + 1) / 2) != self.__rows or int((col + 1) / 2) != self.__cols:
            raise ValueError('Entities str must have the same dimensions as the World str')

    def print(self):
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (row, col)
                res += self.__world_states[state]
            res += '\n'
        print(res)

    def get_world_token(self, state: tuple) -> str | None:
        if state in self.__world_states:
            return self.__world_states[state]
        return None

    def get_entity_token(self, state: tuple) -> str | None:
        if state in self.__entities_states:
            return self.__entities_states[state]
        return None

    @property
    def start(self):
        return self.__start

    @property
    def goals(self):
        return self.__goals

    @property
    def world_states(self):
        return list(self.__world_states.keys())

    @property
    def entities_states(self):
        return list(self.__world_states.keys())

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols


class NewWorld:
    def __init__(self, width: int, height: int, scaling: int, world: {int: WorldEntity}):
        self.__parse_world(width, height, scaling)
        self.__parse_world_lines(world)
        self.__nb_world_states = len(self.__world_states)

        def __parse_world(self, width: int, height: int, scaling: int):
            self.__world_states = {}
            self.__rows = height
            self.__cols = width
            self.__scaling = scaling
            pass

    def __parse_world_lines(self, str_world: {int: WorldEntity}):
        self.__world_states = {}
        row = 0
        col = 0
        for row, line in enumerate(str_world.strip().splitlines()):
            for col, char in enumerate(line):
                self.__world_states[(row, col)] = char

        self.__rows = int((row + 1) / 2)
        self.__cols = int((col + 1) / 2)

    def print(self):
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (row, col)
                res += self.__world_states[state]
            res += '\n'
        print(res)

    def get_world_token(self, state: tuple) -> str | None:
        if state in self.__world_states:
            return self.__world_states[state]
        return None

    @property
    def world_states(self):
        return list(self.__world_states.keys())

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols
