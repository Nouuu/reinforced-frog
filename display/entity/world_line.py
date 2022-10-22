from random import Random
from typing import Dict, List

from display.entity.world_entity import WorldEntity


class WorldLine:
    def __init__(self, width: int, scaling: int, line_type: WorldEntity, entities_min_spacing: int,
                 speed: float, direction: int, spawn_rate: float, entities: List[WorldEntity], random: Random):
        self.__speed_counter = 0
        self.__move_factor = 0
        self.__spawned_entities: Dict[int, WorldEntity] = {}
        self.__line_type = line_type
        self.__entities_min_spacing = entities_min_spacing
        self.__speed = speed
        self.__direction = direction
        self.__spawn_rate = spawn_rate
        self.__entities = entities
        self.__width = width
        self.__scaling = scaling
        self.__random = random
        self.__spawn_initial_entities()

    def __spawn_initial_entities(self):
        if len(self.__entities) == 0:
            return
        entity = self.__random.choice(self.__entities)
        pos = -(self.__scaling * entity.width)
        while pos < self.__width + self.__scaling:
            entity = self.__random.choice(self.__entities)
            rng = round(self.__random.uniform(0, 1), 2)
            if rng < self.__spawn_rate:
                self.__spawned_entities[pos] = entity
                pos += (self.__scaling * entity.width) + self.__entities_min_spacing
            else:
                pos += 1

    def move_entities(self):
        if self.__speed_counter < self.__speed:
            self.__speed_counter += 1
            self.__move_factor = 0
            return
        self.__move_factor = self.__direction
        self.__speed_counter = 0
        new_entities_positions = {}
        for (pos_x, entity) in self.__spawned_entities.items():
            new_pos_x = pos_x + self.__direction
            if self.__width + self.__scaling * entity.width + self.__entities_min_spacing > new_pos_x > -self.__scaling * entity.width - self.__entities_min_spacing:
                new_entities_positions[new_pos_x] = entity
        self.__spawned_entities = new_entities_positions

    def spawn_entity(self):
        if self.__direction == 0 or self.__speed_counter < self.__speed:
            return
        entity = self.__random.choice(self.__entities)
        if self.__direction < 0:
            pos = self.__width + (entity.width * self.__scaling)
            if len(self.spawned_entities.keys()) > 0:
                previous_entity_pos = max(self.spawned_entities.keys())
                if previous_entity_pos + self.spawned_entities[previous_entity_pos].width * self.__scaling + self.__entities_min_spacing > pos:
                    return
        else:
            pos = -(entity.width * self.__scaling)
            if len(self.spawned_entities.keys()) > 0:
                previous_entity_pos = min(self.spawned_entities.keys())
                if previous_entity_pos < pos + (entity.width * self.__scaling + self.__entities_min_spacing):
                    return
        rng = round(self.__random.uniform(0, 1), 2)
        if rng < self.__spawn_rate:
            self.__spawned_entities[pos] = entity

    @property
    def line_type(self) -> WorldEntity:
        return self.__line_type

    @property
    def spawned_entities(self):
        return self.__spawned_entities

    @property
    def move_factor(self):
        return self.__move_factor

    @property
    def direction(self):
        return self.__direction
