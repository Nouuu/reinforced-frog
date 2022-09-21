from conf.config import *


class World:
    def __init__(self, str_world):
        self.__parse(str_world)
        self.__nb_states = len(self.__states)

    def __parse(self, str_world):
        self.__states = {}
        self.__goals = []
        row = 0
        col = 0
        for row, line in enumerate(str_world.strip().splitlines()):
            for col, char in enumerate(line):
                if char == START_TOKEN:
                    self.__start = (row, col)
                elif char == EXIT_TOKEN:
                    self.__goals.append((row, col))
                self.__states[(row, col)] = char

        self.__rows = row + 1
        self.__cols = col + 1

    def print(self):
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (row, col)
                res += self.__states[state]
            res += '\n'
        print(res)

    def get_token(self, state: tuple):
        if state in self.__states:
            return self.__states[state]
        return None

    @property
    def start(self):
        return self.__start

    @property
    def goals(self):
        return self.__goals

    @property
    def states(self):
        return list(self.__states.keys())

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols
