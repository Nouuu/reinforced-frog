from conf.config import *
from game.utils import get_collisions, is_in_safe_zone_on_water


class World:
    def __init__(self,
                 width: int,
                 height: int,
                 scaling: int,
                 world_lines: [WorldLine],
                 player: (tuple, WorldEntity)):
        self.__setup_world(width, height, scaling, player)
        self.__parse_world_lines(world_lines)
        self.__update_world_entities(world_lines)

    def __setup_world(self, width: int, height: int, scaling: int, player: (tuple, WorldEntity)):
        self.__world_states: {(int, int): WorldEntity} = {}
        self.__world_entities_states: {(int, int): WorldEntity} = {}
        self.__player: WorldEntity = player[1]
        self.__player_state: (int, int) = player[0]
        self.__rows = height
        self.__cols = width
        self.__scaling = scaling

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
                self.__world_entities_states[((index * self.__scaling)+self.__scaling // 2, pos_x)] = entity

    def print(self):
        # res = ''
        # for row in range(self.__rows):
        #     for col in range(self.__cols):
        #         state = (row, col)
        #         if state == self.__player_state:
        #             res += self.__player.token
        #         elif state in self.__world_entities_states:
        #             res += self.__world_entities_states[state].token
        #         elif state in self.__world_states:
        #             res += self.__world_states[state].token
        #         else:
        #             res += EMPTY_TOKEN
        #     res += '\n'
        # print(res)
        print('Player position: {}'.format(self.__player_state))
        print('Player collisions :')
        print('From ground :\n-------------------')
        for state in get_collisions(self.__player, self.__player_state, self.__world_states,
                                    self.__world_entities_states,
                                    self.__scaling):
            if state in self.__world_states:
                print(state, '->', self.__world_states[state].token)

        print('-------------------\nFrom entities :')
        for state in get_collisions(self.__player, self.__player_state, self.__world_states,
                                    self.__world_entities_states,
                                    self.__scaling):
            if state in self.__world_entities_states:
                print(state, '->', self.__world_entities_states[state].token)

        print('-------------------\nIs in safe zone :')
        print(
            is_in_safe_zone_on_water(self.__player, self.__player_state, self.__world_entities_states, self.__scaling))

    def get_world_line_entity(self, state: (int, int)) -> WorldEntity | None:
        if state in self.__world_states:
            return self.__world_states[state]
        return None

    def get_world_entity(self, state: (int, int)) -> WorldEntity | None:
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
    def player_state(self):
        return self.__player_state

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
