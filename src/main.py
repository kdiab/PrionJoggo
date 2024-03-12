import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from twitchio.ext import commands, pubsub
import twitchio
import random
import config 
import settings
from controller import HotPotatoGame
from aiohttp import ClientSession



hp = HotPotatoGame()

class Bot(commands.Bot):
    
    async def timeout_user(self, channel_name, user, duration):
        user_id = await self.get_user_id(user)
        # Ensure you're using the correct headers for authentication with the streamer's OAuth token
        headers = {
            'Client-ID': config.STREAMER_CLIENT_ID,
            'Authorization': f'Bearer {config.STREAMER_OAUTH_TOKEN}',
            'Content-Type': 'application/json'
        }
        # Construct the Twitch API endpoint for issuing a timeout
        url = f"https://api.twitch.tv/helix/moderation/bans?broadcaster_id={config.STREAMER_CHANNEL_ID}&moderator_id={config.STREAMER_CHANNEL_ID}"
        data = {
            'data': {
                'user_id': str(user_id),
                'duration': duration * 60,  # Duration in seconds
                'reason': 'Lost at HotPotato L BOZO SMOKED'
            }
        }
        print(data)
        async with self.session.post(url, headers=headers, json=data) as resp:
            if resp.status == 204:
                print(f"Successfully timed out {user} for {duration} seconds.")
            else:
                response = await resp.text()
                print(f"Failed to timeout {user}. Response: {response}")

    async def get_user_id(self, username):
        url = f"https://api.twitch.tv/helix/users?login={username}"
        headers = {
            'Client-ID': config.STREAMER_CLIENT_ID,
            'Authorization': f'Bearer {config.STREAMER_OAUTH_TOKEN}'
        }
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                users = data.get('data', [])
                if users:
                    return users[0].get('id')  # Return the user ID of the first user found
        return None
    
    

  #  async def send_message_as_streamer(self, channel_name: str, message: str):
  #      url = "https://api.twitch.tv/helix/chat/messages"
  #      headers = {
  #          "Authorization": f"Bearer {config.STREAMER_OAUTH_TOKEN}",
  #          "Client-Id": f"{config.STREAMER_CLIENT_ID}",
  #          "Content-Type": "application/json"
  #      }
  #      payload = {
  #          "message": message,
  #          "broadcaster_id": config.STREAMER_CHANNEL_ID,
  #          "sender_id": config.STREAMER_CHANNEL_ID
  #      }
  #      async with aiohttp.ClientSession() as session:
  #          async with session.post(url, json=payload, headers=headers) as response:
  #              response_json = await response.json()  # Parse JSON response
  #              if response.status in [200, 204]:
  #                  print("Message sent successfully as the streamer.")
  #              elif "is_sent" in response_json.get("data", [{}])[0]:
  #                  print(f"Message sent successfully as the streamer: {response_json['data'][0]['message_id']}")
  #              else:
  #                  print(f"Failed to send message as the streamer: {response.text}")
    
    def __init__(self):
        super().__init__(token=config.BOT_OAUTH_TOKEN, prefix=['!'], initial_channels=[config.TARGET_CHANNEL])  # Bot's OAuth token
        self.client = twitchio.Client(token=config.STREAMER_OAUTH_TOKEN)  # Streamer's OAuth token for PubSub
        self.client.pubsub = pubsub.PubSubPool(self.client)
        self.session = None 

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
            display_name = event.user.name.lower()
            hot_potato = event.reward.title

            if hot_potato == settings.REDEMPTION_NAME:
               channel = self.get_channel(config.TARGET_CHANNEL)
               chatters = channel.chatters
               players = [user.name for user in chatters]
               result = await hp.start_game(players, display_name)
               if result == 1:
                   potato_holder = hp.get_current_holder()
                   channel = self.get_channel(config.TARGET_CHANNEL)
                   await channel.send(f"@{potato_holder} you have the potato 🥔! Pass it to anyone in the chat!")
               else:
                   await channel.send("Could not heat up the potato, a game might already be in progress or there is no one in the chat.")

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        self.session = ClientSession()

        # Setup and start PubSub listening
        await self.setup_pubsub()

    async def event_disconnect(self):
        if self.session:
            await self.session.close()

    async def event_message(self, message):
        if message.echo:
            return
        if message.content.lower().startswith('@prisonjoe'):
            channel = self.get_channel(config.TARGET_CHANNEL)
            #print((random.choice(settings.REPLY_MESSAGES)))
            await channel.send(random.choice(settings.REPLY_MESSAGES))

        if message.content.lower().startswith('1'):
            channel = self.get_channel(config.TARGET_CHANNEL)
            chatters = channel.chatters
            players = [user.name for user in chatters]
            result = await hp.start_game(players, message.author.name.lower())
            if result == 1:
                potato_holder = hp.get_current_holder()
                await channel.send(f"@{potato_holder} you have the potato 🥔! Pass it to anyone in chat!")
                #print(f"@{potato_holder} you have the potato 🥔! Pass it to anyone in chat!")
            else:
                await channel.send("Error starting game, a game might already be in progress")
                #print("Error starting game, a game might already be in progress")
        
        if hp.is_game_active():
            if message.content.startswith('@'):
                user = message.author.name.lower()
                target = message.content[1:].split(' ')[0].lower()
                result, timeout = hp.pass_potato(user, target)
                if (result == 1):
                    emote = random.choice(settings.HOT_POTATO_EMOTES)
                    channel = self.get_channel(config.TARGET_CHANNEL)
                    await channel.send(f"{emote} FBCatch 🥔⏳ {hp.time_left()}s... ⌛ @{user} -> @{target} PauseChamp timeout: {timeout} minutes.")
                    #print(f"{emote} FBCatch 🥔⏳ {hp.time_left()}s... ⌛ @{user} -> @{target} PauseChamp timeout: {timeout} minutes.")
                elif result == 2:
                    await channel.send(f"@{user} you cannot pass the potato to yourself!")
                    #print(f"@{user} you cannot pass the potato to yourself!")
                elif result == 3:
                    await channel.send(f"@{user} your target has recently had the potato, try someone else!")
                    #print(f"@{user} your target has recently had the potato, try someone else!")
                elif result == 4:
                    await channel.send(f"@{user} you cannot pass the potato to that user, try someone else.")
                    #print(f"@{user} you cannot pass the potato to that user, try someone else.")

        ban_user = hp.get_last_holder()
        if ban_user != 0:
            emote = random.choice(settings.HOT_POTATO_EMOTES)
            channel = self.get_channel(config.TARGET_CHANNEL)
            await channel.send(f"{emote} 🥔💥💣 @{ban_user[0]} 🥔💥💣 YER BANNED")
            print(f"Timed out {ban_user[0]} for {ban_user[1]} minutes")
            await self.timeout_user(config.TARGET_CHANNEL, ban_user[0], ban_user[1])

        
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

