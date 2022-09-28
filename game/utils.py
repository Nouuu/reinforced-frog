from display.entity.world_entity import WorldEntity


def get_positions(state: tuple, entity: WorldEntity, scaling: int) -> [tuple]:
    positions = set()
    for y in range((scaling * entity.height // 2 + scaling * entity.height % 2)):
        for x in range((scaling * entity.width // 2 + scaling * entity.width % 2)):
            positions.add((state[0] + y, state[1] + x))
            positions.add((state[0] - y, state[1] + x))
            positions.add((state[0] + y, state[1] - x))
            positions.add((state[0] - y, state[1] - x))
    return positions


def get_collisions(entity: WorldEntity, entity_state: tuple, world_line_entities: {tuple: WorldEntity},
                   world_entities: {tuple: WorldEntity},
                   scaling: int) -> [tuple]:
    collisions = set()
    state_positions = get_positions(entity_state, entity, scaling)

    for entity_state in world_line_entities.keys():
        entity_positions = get_positions(entity_state, world_line_entities[entity_state], scaling)
        if any([any([pos in entity_positions for pos in state_positions])]):
            collisions.add(entity_state)
    for entity_state in world_entities.keys():
        entity_positions = get_positions(entity_state, world_entities[entity_state], scaling)
        if any([any([pos in entity_positions for pos in state_positions])]):
            collisions.add(entity_state)

    return collisions


def is_in_safe_zone_on_water(entity: WorldEntity, entity_state: tuple, world_entities: {tuple: WorldEntity},
                             scaling: int) -> bool:
    state_positions = get_positions(entity_state, entity, scaling)

    entities_positions = set()
    for entity_state in world_entities.keys():
        for state in get_positions(entity_state, world_entities[entity_state], scaling):
            entities_positions.add(state)

    for pos in state_positions:
        if pos not in entities_positions:
            return False
    return True
