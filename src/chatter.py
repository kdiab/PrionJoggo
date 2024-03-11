import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from twitchio.ext import commands, pubsub
import twitchio
import random
import dev as config 
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
            display_name = event.user.name
            hot_potato = event.reward.title

            if hot_potato == settings.REDEMPTION_NAME:
               channel = self.get_channel(config.TARGET_CHANNEL)
               chatters = channel.chatters
               players = [user.name for user in chatters]
               result = await hp.start_game(players, display_name)
               if result == 1:
                   potato_holder = hp.get_current_holder()
                   channel = self.get_channel(config.TARGET_CHANNEL)
                   print(f"@{potato_holder} you have the potato 🥔! Pass it to anyone in chat!")
                   #await channel.send(f"@{potato_holder} you have the potato 🥔! Pass it to anyone in chat!")
               else:
                   potato_holder = hp.get_current_holder()
                   if potato_holder == message.author.name.lower():
                       print("Error starting game, a game might already be in progress")
                       #await channel.send("Could not heat up the potato, a game might already be in progress or there is no one in the chat.")

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

        if message.content.lower().startswith('1'):
            channel = self.get_channel(config.TARGET_CHANNEL)
            chatters = channel.chatters
            players = [user.name for user in chatters]
            result = await hp.start_game(players, message.author.name)
            if result == 1:
                potato_holder = hp.get_current_holder()
                channel = self.get_channel(config.TARGET_CHANNEL)
                #await channel.send(f"@{potato_holder} you have the potato 🥔! Pass it to anyone in chat!")
                print(f"@{potato_holder} you have the potato 🥔! Pass it to anyone in chat!")
            else:
                print("Error starting game, a game might already be in progress")
        
        if hp.is_game_active():
            if message.content.startswith('@'):
                user = message.author.name.lower()
                target = message.content[1:].split(' ')[0].lower()
                result, timeout = hp.pass_potato(user, target)
                if (result == 1):
                    emote = random.choice(settings.HOT_POTATO_EMOTES)
                    channel = self.get_channel(config.TARGET_CHANNEL)
                    print(f"{emote} FBCatch 🥔⏳ {hp.time_left()}s... ⌛ @{user} -> @{target} PauseChamp timeout: {timeout} minutes.")
                    #await channel.send(f"{emote} FBCatch 🥔⏳ {hp.time_left()}s... ⌛ @{user} -> @{target} PauseChamp {timeout}")
            elif result == 2:
                    print(f"@{user} you cannot pass the potato to yourself!")
            elif result == 3:
                    print(f"@{user} your target has recently had the potato, try someone else!")

        ban_user = hp.get_last_holder()
        if ban_user != 0:
            emote = random.choice(settings.HOT_POTATO_EMOTES)
            print(f"{emote} 🥔💥💣 @{ban_user[0]} 🥔💥💣 YER BANNED")
            print(f"Timed out {ban_user[0]} for {ban_user[1]} minutes")
        
        await self.handle_commands(message)

    @commands.command()
    async def kiss(self, ctx: commands.Context):
        kissed_user = random.choice(self.getChatters(ctx.users, ctx.author.name))
        msg = random.choice(settings.KISS_MESSAGES)
        msg = msg.replace('{x}', ctx.author.name).replace('{y}', kissed_user)
        print(msg)
        #await ctx.send(msg)

    def getChatters(self, users, author):
        sanitized_users = [user.name for user in users]
        if author in sanitized_users:
            sanitized_users.remove(author)
        return sanitized_users

bot = Bot()
bot.run()

