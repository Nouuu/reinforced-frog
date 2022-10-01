import random

from display.entity.world_entity import WorldEntity


class WorldLine:
    def __init__(self, width: int, scaling: int, line_type: WorldEntity, entities_min_spacing: int,
                 speed: float, direction: int, spawn_rate: float, entities: [WorldEntity]):
        self.__spawned_entities: {int: WorldEntity} = {}
        self.__line_type = line_type
        self.__entities_min_spacing = entities_min_spacing
        self.__speed = speed
        self.__direction = direction
        self.__spawn_rate = spawn_rate
        self.__entities = entities
        self.__width = width
        self.__scaling = scaling
        self.__spawn_initial_entities()

    def __spawn_initial_entities(self):
        if len(self.__entities) == 0:
            return
        pos = -self.__scaling
        while pos < self.__width + self.__scaling:
            rng = round(random.uniform(0, 1), 2)
            if rng < self.__spawn_rate:
                self.__spawned_entities[pos] = random.choice(self.__entities)
                pos += (self.__scaling * self.__spawned_entities[pos].width) + self.__entities_min_spacing
            else:
                pos += 1

    def move_entities(self):
        new_entities_positions = {}
        for (pos_x, entity) in self.__spawned_entities.items():
            new_pos_x = pos_x + (self.__speed * self.__direction)
            if self.__width+self.__scaling > new_pos_x > -self.__scaling:
                new_entities_positions[new_pos_x] = entity
        self.__spawned_entities = new_entities_positions

    @property
    def line_type(self) -> WorldEntity:
        return self.__line_type

    @property
    def spawned_entities(self):
        return self.__spawned_entities
