import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import random
import asyncio 
import time

#import config 
import settings


class HotPotatoGame:
    def __init__(self):
        self.potato_holder = None
        self.game_active = False
        self.game_duration = settings.GAME_DURATION * 60
        self.last_holder = None
        self.timeout_duration = settings.TIMEOUT_DURATION
        self.recent_holders = []
        self.ignore_list = settings.IGNORE_USERS

    async def start_game(self, users, redeemer):
        if not self.game_active:
            self.active_users = users
            print(users)
            if not self.active_users:
                return 0
            self.game_active = True
            self.potato_holder = redeemer 
            self.total_game_duration = self.game_duration + time.time()
            self.timeout_duration = settings.TIMEOUT_DURATION
            self.recent_holders = []
            asyncio.create_task(self.run_game_duration())  # Start the game duration handling as a background task
            return 1
        return 0

    async def run_game_duration(self):
        await asyncio.sleep(self.game_duration)
        await self._internal_end_game()
        
    def pass_potato(self, current_user, target_user):
        if self.game_active and current_user == self.potato_holder and target_user in self.active_users and current_user != target_user and target_user not in self.recent_holders and target_user not in self.ignore_list:
            print(f'{current_user} -> {target_user}')
            self.potato_holder = target_user
            self.recent_holders.append(current_user)
            if len(self.recent_holders) > 3:
                self.recent_holders.pop(0)
            self.timeout_duration += 1
            print(f'timeout duration increased to {self.timeout_duration} minutes')
            return 1, self.timeout_duration
        if self.game_active and current_user == target_user:
            return 2, self.timeout_duration
        if self.game_active and target_user in self.recent_holders:
            return 3, self.timeout_duration
        if self.game_active and target_user in self.ignore_list:
            return 4, self.timeout_duration


        return 0, self.timeout_duration

    async def _internal_end_game(self):
        self.game_active = False
        self.game_ended = True
        self.last_holder = self.potato_holder  # Capture the last holder before resetting
        self.potato_holder = None
        print("Game ended")

    def get_last_holder(self):
        if not self.game_active and self.last_holder:
            ban_this_guy = self.last_holder
            self.last_holder = None
            return ban_this_guy, self.timeout_duration
        return 0

    def get_current_holder(self):
        if self.potato_holder:
            return self.potato_holder

    def is_game_active(self):
        return self.game_active

    def time_left(self):
        return int(self.total_game_duration - time.time())
