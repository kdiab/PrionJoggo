import config.twitch_settings
from twitchio.ext import commands

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=config.twitch_settings.TWITCH_BOT_OAUTH_TOKEN,
            client_id=config.twitch_settings.TWITCH_CLIENT_ID,
            nick=config.twitch_settings.TWITCH_BOT_USERNAME,
            prefix='!',
            initial_channels=[config.twitch_settings.TWITCH_BOT_USERNAME]
        )

    async def event_ready(self):
        print(f'Logged in as {self.nick}')

    async def event_message(self, message):
        print(f'[{message.channel.name}] {message.author.name}: {message.content}')
        await self.handle_commands(message)

    async def event_command_error(self, ctx, error):
        print(f'Error: {error}')

