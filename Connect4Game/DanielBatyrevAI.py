import Connect4Game as Game
import random


class RandomStrategy(Game.Connect4GameStrategy):
    def __init__(self, name="Daniel Batyrev"):
        self.name = name

    @classmethod
    def strategy(cls, game_safety_copy):
        valid_moves = list()
        for col in range(7):
            if game_safety_copy.is_valid_move(col):
                valid_moves.append(col)
        return random.choice(valid_moves)
