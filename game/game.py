from game.Player import Player
from game.world import World


class Game:
    def __init__(self, world: World, players: [Player], player_init_state: (int, int)):
        self.__world = world
        self.__players = players
        self.__player_init_state = player_init_state

    def start(self):
        for player in self.__players:
            player.init(self.__world, self.__player_init_state)

    def step(self):
        for player in self.__players:
            action = player.best_move()
            reward, new_state = self.__world.step(player.state, action, player.world_entity)
            player.step(action, reward, new_state)

    def human_step(self, action: (int, int)):
        for player in self.__players:
            if player.is_human:
                reward, new_state = self.__world.step(player.state, action, player.world_entity)
                player.step(action, reward, new_state)
                break

    @property
    def world(self):
        return self.__world

    @property
    def players(self):
        return self.__players
