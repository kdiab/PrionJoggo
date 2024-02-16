import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import random
import threading

#import config 
import settings


class HotPotatoGame:
    def __init__(self):
        self.potato_holder = None
        self.game_active = False
        self.game_duration = settings.GAME_DURATION
        self.game_timer = None

    def start_game(self, users):
        """Start the Hot Potato game with a dynamic list of users. Returns 1 on success, 0 on failure."""
        if not self.game_active:
            self.active_users = users
            self.game_active = True
            self.potato_holder = random.choice(self.active_users)
            self.potato_holder = "djkumboi" 
            print(self.potato_holder)
            self.game_timer = threading.Timer(self.game_duration, self.end_game)
            self.game_timer.start()
            return 1  # Success
        else:
            return 0  # Failure due to an already active game

    def pass_potato(self, current_user, target_user):
        """Pass the hot potato to another user. Returns 1 on success, 0 on failure."""
        if self.game_active and current_user == self.potato_holder  and target_user in self.active_users and current_user != target_user:
            self.potato_holder = target_user
            return 1  # Success
        else:
            return 0  # Failure due to game not active or user not valid

   def end_game(self):
    """End the Hot Potato game and return the name of the last potato holder."""
    if self.game_active:
        self.game_active = False
        if self.game_timer is not None:
            self.game_timer.cancel()
        last_holder = self.potato_holder  # Capture the name of the last holder before ending the game
        self.potato_holder = None  # Reset the potato holder for the next game
        return 1, last_holder  # Return success and the last holder's name
    return 0, None  # Return failure and None if no game was active

    def is_game_active(self):
        """Check if the game is currently active."""
        return self.game_active

