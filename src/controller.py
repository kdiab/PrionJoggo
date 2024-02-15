import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import random
import threading

#import config 
import settings


class HotPotatoGame:
    def __init__(self):
        self.potato_holder = None  # This line was missing in the previous version
        self.game_active = False
        self.game_duration = settings.GAME_DURATION
        self.game_timer = None

    def start_game(self, users):
        """Start the Hot Potato game with a dynamic list of users. Returns 1 on success, 0 on failure."""
        if not self.game_active:
            self.active_users = users
            self.game_active = True
            self.potato_holder = random.choice(self.active_users)
            self.game_timer = threading.Timer(self.game_duration, self.end_game)
            self.game_timer.start()
            return 1  # Success
        else:
            return 0  # Failure due to an already active game

    def pass_potato(self, target_user):
        """Pass the hot potato to another user. Returns 1 on success, 0 on failure."""
        if self.game_active and target_user in self.active_users:
            self.potato_holder = target_user
            return 1  # Success
        else:
            return 0  # Failure due to game not active or user not valid

    def end_game(self):
        """End the Hot Potato game. Automatically called after game duration expires."""
        if self.game_active:
            self.game_active = False
            if self.game_timer is not None:
                self.game_timer.cancel()
            return 1  # Success
        return 0  # No active game to end

