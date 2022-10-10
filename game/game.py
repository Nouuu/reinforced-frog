from conf.config import ACTION_MOVES
from game.Player import Player
from game.world import World


class Game:
    def __init__(self, world: World, players: [Player], player_init_state: (int, int), auto_start: bool = True):
        self.__world = world
        self.__players = players
        self.__player_init_state = player_init_state
        self.__auto_start = auto_start

    def start(self):
        for player in self.__players:
            self.init_player(player)

    def init_player(self, player):
        player.init(self.__world, self.__player_init_state,
                    self.__world.get_current_environment(self.__player_init_state[0], 3))

    def step(self):
        self.__world.update_entities()
        for player in self.__players:
            action = player.best_move()
            reward, new_state, environment, is_game_over = self.__world.step(player.state, ACTION_MOVES[action],
                                                                             player.world_entity)
            player.step(action, reward, new_state, environment)
            if is_game_over:
                player.save_score()
                if self.__auto_start:
                    self.init_player(player)
                else:
                    self.__game_over(player)

    def human_step(self, action: (int, int)):
        for player in filter(lambda player_f: player_f.is_human, self.__players):
            reward, new_state, environment, is_game_over = self.__world.step(player.state, action, player.world_entity)
            player.step(action, reward, new_state, environment)

    def __game_over(self, player: Player):
        self.__players.remove(player)

    @property
    def world(self):
        return self.__world

    @property
    def players(self):
        return self.__players
