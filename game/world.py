from typing import Dict

import xxhash

from conf.config import *
from game.utils import get_positions, get_collisions, is_in_safe_zone_on_water


class World:
    def __init__(self,
                 width: int,
                 height: int,
                 scaling: int,
                 world_lines: [WorldLine], env: Dict[str, str | float | int | bool]):
        self.__env = env
        self.__setup_world(width, height, scaling)
        self.__parse_world_lines(world_lines)
        self.__update_world_entities(world_lines)

    def __setup_world(self, width: int, height: int, scaling: int):
        self.__world_states: {(int, int): WorldEntity} = {}
        self.__world_entities_states: {(int, int): WorldEntity} = {}
        self.__rows = height
        self.__cols = width
        self.__scaling = scaling
        self.__history: [str] = []

    def __parse_world_lines(self, world_lines: [WorldLine]):
        self.__world_lines = world_lines
        for row in range(self.__scaling // 2, self.__rows, self.__scaling):
            for col in range(self.__scaling // 2, self.__cols, self.__scaling):
                state = (row, col)
                self.__world_states[state] = world_lines[row // self.__scaling].line_type

    def __update_world_entities(self, world_lines: [WorldLine]):
        self.__world_entities_states: {(int, int): WorldEntity} = {}
        for (index, world_line) in enumerate(world_lines):
            for (pos_x, entity) in world_line.spawned_entities.items():
                self.__world_entities_states[((index * self.__scaling) + (self.__scaling // 2), pos_x)] = entity

    def __is_forbidden_state(self, new_state, world_entity: WorldEntity) -> bool:
        for state in get_positions(new_state, world_entity, self.__scaling):
            if not 0 <= state[0] < self.__rows or not 0 <= state[1] < self.__cols:
                return True
        for state in get_collisions(world_entity, new_state, self.__world_states,
                                    self.__world_entities_states,
                                    self.__scaling):
            if state in self.__world_states:
                if self.__world_states[state].token in FORBIDDEN_STATES \
                    and (
                    self.__world_states[state].token != WATER_TOKEN
                    or not is_in_safe_zone_on_water(world_entity, new_state, self.__world_entities_states,
                                                    self.__scaling)
                ):
                    return True
            if state in self.__world_entities_states:
                if self.__world_entities_states[state].token in FORBIDDEN_STATES:
                    return True
        return False

    def __is_on_ground(self, new_state: (int, int), world_entity: WorldEntity) -> bool:
        for state in get_collisions(world_entity, new_state, self.__world_states,
                                    self.__world_entities_states,
                                    self.__scaling):
            if state in self.__world_states and self.__world_states[state].token == GROUND_TOKEN:
                return True
        return False

    def __filter_states(self, states: {(int, int): WorldEntity}, current_state: (int, int), number_of_lines: int,
                        cols_arround: int) -> {
        (int, int): WorldEntity}:
        min_line = max(current_state[0] - (number_of_lines * self.__scaling) - self.__scaling // 2, 0)
        max_line = min(current_state[0] + 1 * self.__scaling + self.__scaling // 2, self.__rows - 1)
        min_col = max(current_state[1] - cols_arround, 0)
        max_col = min(current_state[1] + cols_arround, self.__cols - 1)
        return dict(filter(lambda state: min_line <= state[0][0] < max_line and min_col <= state[0][1] < max_col,
                           states.items()))

    def __world_str(self, current_state: (int, int), number_of_lines: int, cols_arround: int) -> str:
        min_line = max(current_state[0] - (number_of_lines * self.__scaling) - self.__scaling // 2, 0)
        max_line = min(current_state[0] + 1 * self.__scaling + self.__scaling // 2, self.__rows - 1)
        min_col = max(current_state[1] - cols_arround, 0)
        max_col = min(current_state[1] + cols_arround, self.__cols - 1)
        world_str = ''
        # print(f"current_line: {current_state[0]}, min_line: {min_line}, max_line: {max_line}")
        filtered_world_states = self.__filter_states(self.__world_states, current_state, number_of_lines,
                                                     cols_arround)
        filtered_world_entities_states = self.__filter_states(self.__world_entities_states, current_state,
                                                              number_of_lines, cols_arround)
        for row in range(min_line, max_line):
            for col in range(min_col, max_col):
                if (row, col) in filtered_world_states:
                    world_str += filtered_world_states[(row, col)].token
                else:
                    world_str += ' '
                if (row, col) in filtered_world_entities_states:
                    world_str += filtered_world_entities_states[(row, col)].token
                else:
                    world_str += ' '
            world_str += '\n'
        return world_str

    def __hash_world_states(self, history: int) -> bytes:
        return xxhash.xxh3_64_digest('|'.join(self.__history[-history:]))

    def get_current_environment(self, current_state: (int, int), number_of_lines: int, cols_arround: int) -> bytes:
        return xxhash.xxh3_64_digest(self.__world_str(current_state, number_of_lines, cols_arround))

    def print(self):
        pass
        # print('Player position: {}'.format(self.__player_state))
        # print('Player collisions :')
        # print('From ground :\n-------------------')
        # for state in get_collisions(self.__player, self.__player_state, self.__world_states,
        #                             self.__world_entities_states,
        #                             self.__scaling):
        #     if state in self.__world_states:
        #         print(state, '->', self.__world_states[state].token)
        #
        # print('-------------------\nFrom entities :')
        # for state in get_collisions(self.__player, self.__player_state, self.__world_states,
        #                             self.__world_entities_states,
        #                             self.__scaling):
        #     if state in self.__world_entities_states:
        #         print(state, '->', self.__world_entities_states[state].token)
        #
        # print('-------------------\nIs in safe zone :')
        # print(
        #     is_in_safe_zone_on_water(self.__player, self.__player_state, self.__world_entities_states, self.__scaling))

    def get_world_line_entity(self, state: (int, int)) -> WorldEntity | None:
        if state in self.__world_states:
            return self.__world_states[state]
        return None

    def get_world_entity(self, state: (int, int)) -> WorldEntity | None:
        if state in self.__world_entities_states:
            return self.__world_entities_states[state]
        return None

    def step(self, state: (int, int), action: (int, int), world_entity: WorldEntity) -> (
        float, (int, int), bytes, bool):
        new_state = (state[0] + action[0] * self.__scaling, state[1] + action[1] * self.__scaling // 3)
        reward = -1 * (self.__rows / new_state[0])
        is_game_over = False

        if self.__is_forbidden_state(new_state, world_entity):
            new_state = state
            reward = -2 * self.__cols * self.__rows  # * (new_state[0] / self.__rows)
            is_game_over = True
        elif self.__is_win_state(new_state, world_entity):
            reward = self.__cols * self.__rows
            is_game_over = True
        elif self.__is_on_ground(new_state, world_entity) and self.__is_on_ground(state, world_entity) \
            and action == (0, 0):  # punir plus s'il RESTE sur une zone safe
            reward -= 1

        self.__history.append(self.__world_str(new_state, self.__env['AGENT_VISIBLE_LINES_ABOVE'],
                                               self.__env['AGENT_VISIBLE_COLS_ARROUND']))
        return reward, new_state, self.__hash_world_states(self.__env['AGENT_QTABLE_HISTORY']), is_game_over

    def update_entities(self):
        for world_line in self.__world_lines:
            world_line.spawn_entity()
            world_line.move_entities()
        self.__update_world_entities(self.__world_lines)

    @property
    def world_states(self):
        return list(self.__world_states.keys())

    @property
    def world_entities_states(self):
        return list(self.__world_entities_states.keys())

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols

    def __is_win_state(self, new_state, world_entity: WorldEntity) -> bool:
        for state in get_collisions(world_entity, new_state, self.__world_states,
                                    self.__world_entities_states,
                                    self.__scaling):
            if state in self.__world_states and self.__world_states[state].token in WIN_STATES:
                return True
        return False
