from typing import Tuple, List, Dict
from conf.config import WorldEntity, WorldLine
from game.utils import get_positions


class World:
    def __init__(
        self,
        width: int,
        height: int,
        scaling: int,
        world_lines: List[WorldLine],
        player: Tuple[Tuple[int, int], WorldEntity]
    ):
        self.__setup_world(width, height, scaling)
        self.__parse_world_lines(world_lines)
        self.__update_world_entities(world_lines)

    def __setup_world(self, width: int, height: int, scaling: int):
        self.__world_states: Dict[Tuple[int, int]: WorldEntity] = {}
        self.__world_entities_states: Dict[Tuple[int, int]: WorldEntity] = {}
        self.__rows = height
        self.__cols = width
        self.__scaling = scaling

    def __parse_world_lines(self, world_lines: List[WorldLine]):
        self.__world_lines = world_lines
        for row in range(self.__scaling // 2, self.__rows, self.__scaling):
            for col in range(self.__scaling // 2, self.__cols, self.__scaling):
                state = (row, col)
                self.__world_states[state] = world_lines[row // self.__scaling].line_type

    def __update_world_entities(self, world_lines: List[WorldLine]):
        self.__world_entities_states: {Tuple[int, int]: WorldEntity} = {}
        for (index, world_line) in enumerate(world_lines):
            for (pos_x, entity) in world_line.spawned_entities.items():
                self.__world_entities_states[((index * self.__scaling)+self.__scaling // 2, pos_x)] = entity

    def __is_forbidden_state(self, new_state, world_entity: WorldEntity) -> bool:
        for state in get_positions(new_state, world_entity, self.__scaling):
            if not 0 <= state[0] <= self.__rows or not 0 <= state[1] <= self.__cols:
                return True
        return False

    def get_world_line_entity(self, state: Tuple[int, int]) -> WorldEntity | None:
        if state in self.__world_states:
            return self.__world_states[state]
        return None

    def get_world_entity(self, state: Tuple[int, int]) -> WorldEntity | None:
        if state in self.__world_entities_states:
            return self.__world_entities_states[state]
        return None

    def update_entities(self):
        for world_line in self.__world_lines:
            world_line.spawn_entity()
            world_line.move_entities()
        self.__update_world_entities(self.__world_lines)

    @property
    def player(self):
        return self.__player

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

    @property
    def scailing(self):
        return self.__scaling

