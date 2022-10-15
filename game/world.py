from typing import Tuple

import xxhash

from conf.config import *
from game.utils import get_collisions, is_in_safe_zone_on_water, is_win_state


class World:
    def __init__(self,
                 width: int,
                 height: int,
                 scaling: int,
                 world_lines: List[WorldLine], env: Dict[str, str | float | int | bool]):
        self.__env = env
        self.__setup_world(width, height, scaling)
        self.__parse_world_lines(world_lines)
        self.__update_world_entities()
        self.__setup_entity_matrix()
        self.__update_entity_matrix()

    def __setup_world(self, width: int, height: int, scaling: int):
        self.__world_states: Dict[Tuple[int, int], WorldEntity] = {}
        self.__world_entities_states: Dict[Tuple[int, int], WorldEntity] = {}
        self.__rows = height
        self.__cols = width
        self.__scaling = scaling
        # self.__history: List[str] = []

    def __setup_entity_matrix(self):
        self.__world_line_matrix: list[list[str]] = []
        self.__world_entity_matrix: list[list[str]] = []
        for line in self.__world_lines:
            token = line.line_type.token
            for i in range(0, self.__scaling):
                line_matrix = []
                for j in range(0, self.width):
                    line_matrix.append(token)
                self.__world_line_matrix.append(line_matrix)

    def __update_entity_matrix(self):
        self.__world_entity_matrix: list[list[str]] = [[value for value in line] for line in self.__world_line_matrix]
        for state, entity in self.__world_entities_states.items():
            token = entity.token
            width = entity.width
            height = entity.height
            x = state[1]
            y = state[0]
            x_range = range(x, min(x + width * self.__scaling, self.__cols))
            for i in range(y, min(y + height * self.__scaling, self.__rows)):
                for j in x_range:
                    self.__world_entity_matrix[i][j] = token

    def __parse_world_lines(self, world_lines: List[WorldLine]):
        self.__world_lines = world_lines
        for row in range(0, self.__rows, self.__scaling):
            for col in range(0, self.__cols, self.__scaling):
                state = (row, col)
                self.__world_states[state] = world_lines[row // self.__scaling].line_type

    def __update_world_entities(self):
        self.__world_entities_states: {(int, int): WorldEntity} = {}
        for (index, world_line) in enumerate(self.__world_lines):
            for (pos_x, entity) in world_line.spawned_entities.items():
                self.__world_entities_states[(index * self.__scaling, pos_x)] = entity

    def __is_forbidden_state(self, new_state, world_entity: WorldEntity, collisions: [tuple]) -> bool:
        entity_min_y = new_state[0]
        entity_max_y = new_state[0] + world_entity.height * self.__scaling - 1
        entity_min_x = new_state[1]
        entity_max_x = new_state[1] + world_entity.width * self.__scaling - 1
        if entity_min_y < 0 or entity_max_y > self.height or entity_min_x < 0 or entity_max_x > self.width:
            return True
        for entity_token in collisions:
            if entity_token in FORBIDDEN_STATES and (
                entity_token != WATER_TOKEN or not is_in_safe_zone_on_water(collisions)):
                return True
        return False

    def __is_on_ground(self, new_state: Tuple[int, int], world_entity: WorldEntity) -> bool:
        for token in get_collisions(world_entity, new_state, self.__world_entity_matrix, self.__scaling):
            if token == GROUND_TOKEN or token == START_TOKEN:
                return True
        return False

    def __world_str(self, current_state: Tuple[int, int], number_of_lines: int, cols_arround: int) -> str:
        min_line = current_state[0] - (number_of_lines * self.__scaling)
        max_line = current_state[0] + self.__scaling + 1
        min_col = current_state[1] - cols_arround
        max_col = current_state[1] + self.__scaling + cols_arround
        return '\n'.join(
            ''.join(
                [AGENT_ENVIRONMENT_TOKENS[self.__world_entity_matrix[row][
                    col]] if 0 <= row < self.__rows and 0 <= col < self.__cols else FORBIDDEN_ENTITY_TOKEN for col in
                 range(min_col, max_col)])
            for row in
            range(min_line, max_line, self.__scaling))

    # def __hash_world_states(self, history: int) -> bytes:
    #     if len(self.__history) > history:
    #         self.__history = self.__history[-history:]
    #     return xxhash.xxh32_digest('|'.join(self.__history))

    def get_current_environment(self, current_state: Tuple[int, int], number_of_lines: int, cols_arround: int) -> bytes:
        return xxhash.xxh32_digest(self.__world_str(current_state, number_of_lines, cols_arround)) \
            if self.__env['HASH_QTABLE'] else self.__world_str(current_state, number_of_lines, cols_arround)

    def get_world_line_entity(self, state: Tuple[int, int]) -> WorldEntity | None:
        if state in self.__world_states:
            return self.__world_states[state]
        return None

    def get_world_entity(self, state: Tuple[int, int]) -> WorldEntity | None:
        if state in self.__world_entities_states:
            return self.__world_entities_states[state]
        return None

    def get_world_line(self, state: (int, int)) -> WorldLine:
        return self.__world_lines[state[0] // self.__scaling]

    def step(self, state: Tuple[int, int], action: Tuple[int, int], world_entity: WorldEntity) -> Tuple[
        float,
        Tuple[int, int],
        bytes,
        bytes,
        bool
    ]:
        new_state = (state[0] + action[0] * self.__scaling, state[1] + action[1] * (self.__scaling // 3))
        reward = -1
        is_game_over = False
        environment = self.get_current_environment(new_state, int(self.__env['AGENT_VISIBLE_LINES_ABOVE']),
                                                   int(self.__env['AGENT_VISIBLE_COLS_ARROUND']))
        current_environment = self.get_current_environment(state, int(self.__env['AGENT_VISIBLE_LINES_ABOVE']),
                                                           int(self.__env['AGENT_VISIBLE_COLS_ARROUND']))
        collisions = get_collisions(world_entity, new_state, self.__world_entity_matrix, self.__scaling)
        if self.__is_forbidden_state(new_state, world_entity, collisions):
            new_state = state
            reward = -self.__cols * self.__rows  # * (new_state[0] / self.__rows)
            is_game_over = True
        elif is_win_state(collisions):
            reward = self.__cols * self.__rows
            is_game_over = True
        return reward, \
               new_state, \
               environment, \
               current_environment, \
               is_game_over

    def update_entities(self):
        for world_line in self.__world_lines:
            world_line.spawn_entity()
            world_line.move_entities()
        self.__update_world_entities()
        self.__update_entity_matrix()

    @property
    def world_states(self):
        return list(self.__world_states.keys())

    @property
    def world_entities_states(self):
        return self.__world_entities_states

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols

    @property
    def world_entity_matrix(self):
        return self.__world_entity_matrix

    @property
    def scaling(self):
        return self.__scaling
