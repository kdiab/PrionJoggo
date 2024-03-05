import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from twitchio.ext import commands, pubsub
import twitchio
import random
import config 
import settings
from controller import HotPotatoGame

hp = HotPotatoGame()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=config.BOT_OAUTH_TOKEN, prefix=['!'], initial_channels=[config.TARGET_CHANNEL])  # Bot's OAuth token
        self.client = twitchio.Client(token=config.STREAMER_OAUTH_TOKEN)  # Streamer's OAuth token for PubSub
        self.client.pubsub = pubsub.PubSubPool(self.client)
        
    async def setup_pubsub(self):
        # Define the topics to subscribe to
        topics = [
                pubsub.channel_points(config.STREAMER_OAUTH_TOKEN)[int(config.STREAMER_CHANNEL_ID)],
        ]
        
        # Subscribe to the topics
        await self.client.pubsub.subscribe_topics(topics)
        
        # Listen to channel point redemptions
        @self.client.event()
        async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
            print(event.reward.title)
            #<CustomReward id=582ea7ab-dad0-4030-b839-a5b8a0e5c92b title=Positive Stimuli For Streamer cost=350>
            display_name = event.user.name
            hot_potato = event.reward.title
   
            if hot_potato == settings.REDEMPTION_NAME:
                players = getChatters()
                result = await hp.start_game(players, display_name)
            if result == 1:
                potato_holder = hp.get_current_holder()
                p = ', '.join(players)
                await twitch_instance.send_chat_announcement(streamer_id, streamer_id, f"@{potato_holder} you have the potato 🥔! Pass it to anyone in this list {p}")
                print("Game started")
            else:
                print("Error starting game, a game might already be in progress")

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        
        # Setup and start PubSub listening
        await self.setup_pubsub()

    async def event_message(self, message):
        if message.echo:
            return
        if message.content.lower().startswith('@prisonjoe'):
            channel = self.get_channel(config.TARGET_CHANNEL)
            print((random.choice(settings.REPLY_MESSAGES)))
            
            #await channel.send(random.choice(settings.REPLY_MESSAGES))
        await self.handle_commands(message)

    @commands.command()
    async def kiss(self, ctx: commands.Context):
        kissed_user = random.choice(self.getChatters(ctx.users, ctx.author.name))
        msg = random.choice(settings.KISS_MESSAGES)
        msg = msg.replace('{x}', ctx.author.name).replace('{y}', kissed_user)
        print(msg)
        #await ctx.send(msg)
    
    @commands.command()
    async def k(self, ctx: commands.Context):
        channel = self.get_channel(config.TARGET_CHANNEL)
        chatters = channel.chatters
        user_names = [user.name for user in chatters]
    
    def getChatters(self, users, author):
        sanitized_users = [user.name for user in users]
        if author in sanitized_users:
            sanitized_users.remove(author)
        return sanitized_users

bot = Bot()
bot.run()

