import random

from display.entity.world_entity import WorldEntity


class WorldLine:
    def __init__(self, width: int, scaling: int, line_type: WorldEntity, entities_min_spacing: int,
                 speed: int, direction: tuple, spawn_rate: float, entities: [WorldEntity]):
        self.__line_type = line_type
        self.__entities_min_spacing = entities_min_spacing
        self.__speed = speed
        self.__direction = direction
        self.__spawn_rate = spawn_rate
        self.__entities = entities
        self.__spawn_initial_entities(width, scaling)

    def __spawn_initial_entities(self, width: int, scaling: int):
        self.__spawned_entities: {tuple: WorldEntity} = {}
        if len(self.__entities) == 0:
            return
        pos = -scaling
        while pos < (width - scaling):
            rng = round(random.uniform(0, 1), 2)
            if rng > self.__spawn_rate:
                self.__spawned_entities[(0, pos)] = random.choice(self.__entities)
                pos += scaling + self.__entities_min_spacing
            else:
                pos += 1

    @property
    def line_type(self) -> WorldEntity:
        return self.__line_type
