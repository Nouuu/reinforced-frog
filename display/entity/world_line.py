from display.entity.world_entity import WorldEntity


class WorldLine:
    def __init__(self, width: int, scaling: int, line_type: WorldEntity, entities_min_spacing: int,
                 speed: int, direction: tuple, entities: [WorldEntity]):
        self.__line_type = line_type
        self.__entities_min_spacing = entities_min_spacing
        self.__speed = speed
        self.__direction = direction
        self.__entities = entities
        self.__spawn_initial_entities(width, scaling)

    def __spawn_initial_entities(self, width: int, scaling: int):
        if self.__entities is []:
            self.__spawned_entities = []
        pos = -scaling
        while pos < width - scaling:
            pos += 1

    @property
    def line_type(self) -> WorldEntity:
        return self.__line_type
