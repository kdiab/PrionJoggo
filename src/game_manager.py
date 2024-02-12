import game_logic

class GameManager:
    def __init__(self, twitch_bot):
        self.twitch_bot = twitch_bot
        self.active_game = None

    def start_game(self):
        # Check if there's already an active game
        if self.active_game:
            self.twitch_bot.send_chat_message("There's already an active game.")
            return

        # Start a new game
        self.active_game = game_logic.Game()
        self.active_game.start()

    def pass_potato(self, user, target_user):
        if self.active_game:
            self.active_game.pass_potato(user, target_user)

def init_game_manager(twitch_bot):
    global game_manager_instance
    game_manager_instance = GameManager(twitch_bot)

def start_game():
    game_manager_instance.start_game()

def pass_potato(user, target_user):
    game_manager_instance.pass_potato(user, target_user)

