import twitch_integration
import game_manager

def main():
    # Initialize Twitch bot
    twitch_bot = twitch_integration.TwitchBot()

    # Connect to Twitch chat
    twitch_bot.connect()

    # Initialize game manager
    game_manager.init_game_manager(twitch_bot)

    # Start listening to chat messages
    twitch_bot.listen_chat_messages()

if __name__ == "__main__":
    main()

