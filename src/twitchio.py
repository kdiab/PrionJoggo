from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token='YOUR_OAUTH_TOKEN',
            client_id='YOUR_CLIENT_ID',
            nick='YOUR_BOT_NICKNAME',
            prefix='!',
            initial_channels=['#channel']
        )

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        await self.handle_commands(message)

    @commands.command(name='timeout')
    async def timeout_user(self, ctx):
        if not ctx.author.is_mod:
            return  # Only allow mods to use this command

        target_user = ctx.message.content.split(' ')[1]  # Assumes the command is like "!timeout username"
        await ctx.channel.timeout(user=target_user, duration=300)  # Timeout duration in seconds (300 seconds = 5 minutes)
        await ctx.send(f'{target_user} has been timed out for 5 minutes.')

if __name__ == '__main__':
    bot = Bot()
    bot.run()
