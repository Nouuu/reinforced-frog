import xxhash

from conf.config import *
from game.utils import get_positions, get_collisions, is_in_safe_zone_on_water


class World:
    def __init__(self,
                 width: int,
                 height: int,
                 scaling: int,
                 world: [WorldEntity],
                 world_entities: {tuple: WorldEntity}):
        self.__setup_world(width, height, scaling)
        self.__parse_world_lines(world)
        self.__parse_world_entities(world_entities)

    def __setup_world(self, width: int, height: int, scaling: int):
        self.__world_states: {(int, int): WorldEntity} = {}
        self.__world_entities_states: {(int, int): WorldEntity} = {}
        self.__rows = height
        self.__cols = width
        self.__scaling = scaling
        self.__history: [str] = []

    def __parse_world_lines(self, world: [WorldEntity]):
        for row in range(self.__scaling // 2, self.__rows, self.__scaling):
            for col in range(self.__scaling // 2, self.__cols, self.__scaling):
                state = (row, col)
                self.__world_states[state] = world[row // self.__scaling]

    def __parse_world_entities(self, world: {tuple: WorldEntity}):
        for state in world.keys():
            self.__world_entities_states[state] = world[state]

    def __is_forbidden_state(self, new_state, world_entity: WorldEntity) -> bool:
        for state in get_positions(new_state, world_entity, self.__scaling):
            if not 0 <= state[0] <= self.__rows or not 0 <= state[1] <= self.__cols:
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
            elif state in self.__world_entities_states:
                if self.__world_entities_states[state].token in FORBIDDEN_STATES:
                    return True
        return False

    def __filter_states(self, states: {(int, int): WorldEntity}, current_line: int, number_of_lines) -> {
        (int, int): WorldEntity}:
        return filter(lambda state: (current_line - 1) * self.__scaling <= state[0] < (
            current_line + number_of_lines) * self.__scaling, states)

    def __world_str(self, current_line: int, number_of_lines: int) -> str:
        return \
            ''.join([self.__world_states[state].token for state in
                     self.__filter_states(self.__world_states, current_line, number_of_lines)]) + \
            ''.join([self.__world_entities_states[state].token for state in
                     self.__filter_states(self.__world_entities_states, current_line, number_of_lines)])

    def __hash_world_states(self, history: int) -> bytes:
        return xxhash.xxh3_64_digest('|'.join(self.__history[-history:]))

    def get_current_environment(self, current_line: int, number_of_lines: int) -> bytes:
        return xxhash.xxh3_64_digest(self.__world_str(current_line, number_of_lines))

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
        reward = -1
        is_game_over = False

        if self.__is_forbidden_state(new_state, world_entity):
            new_state = state
            reward = -2 * self.__cols * self.__rows
            is_game_over = True

        if self.__is_win_state():
            is_game_over = True

        self.__history.append(self.__world_str(new_state[0], 3))
        return reward, new_state, self.__hash_world_states(3), is_game_over

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

    def __is_win_state(self) -> bool:
        return False
