import random

class HotPotatoGame:
    def __init__(self, players):
        self.players = players
        self.current_holder = None

    def start_game(self):
        self.current_holder = random.choice(self.players)

    def pass_potato(self, next_player):
        self.current_holder = next_player

    def get_winner(self):
        return self.current_holder
