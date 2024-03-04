import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import time
import random
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from active_user_tracker import ActiveUserTracker

import asyncio
from pprint import pprint
from uuid import UUID
import config 
import settings
from controller import HotPotatoGame

APP_ID = config.APP_ID
APP_SECRET = config.APP_SECRET
BOT_APP_ID = config.BOT_APP_ID
BOT_APP_SECRET = config.BOT_APP_SECRET
CHAT_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_MANAGE_BANNED_USERS, AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS]
USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS]
TARGET_CHANNEL = config.TARGET_CHANNEL

# Initialize the tracker
tracker = ActiveUserTracker()
hp = HotPotatoGame()
streamer_id = None
twitch_instance = None

async def callback_redemptions(uuid: UUID, data: dict) -> None:
    display_name = data['data']['redemption']['user']['display_name']
    hot_potato = data['data']['redemption']['reward']['title']
    print(display_name, 'redeemed', hot_potato)
   
    if hot_potato == settings.REDEMPTION_NAME:
        players = tracker.get_usernames()
        result = await hp.start_game(players, display_name)
        if result == 1:
            potato_holder = hp.get_current_holder()
            p = ', '.join(players)
            await twitch_instance.send_chat_announcement(streamer_id, streamer_id, f"@{potato_holder} you have the potato 🥔! Pass it to anyone in this list {p}")
            print("Game started")
        else:
            print("Error starting game, a game might already be in progress")
 

async def on_ready(ready_event: EventData):
    print('Ready to throw potatoes')
    await ready_event.chat.join_room(TARGET_CHANNEL)

async def on_message(msg: ChatMessage):
    if hp.is_game_active():
        if msg.text.startswith('@'):
            user = msg.user.name.lower()
            target = msg.text[1:].split(' ')[0].lower()
            result = hp.pass_potato(user, target)
            if (result == 1):
                emote = random.choice(settings.HOT_POTATO_EMOTES)
                await msg.chat.send_message(msg.room, f"{emote} FBCatch 🥔⏳ {hp.time_left()}s... ⌛ @{user} -> @{target}")
    
    ban_user = hp.get_last_holder()
    if ban_user != 0:
        emote = random.choice(settings.HOT_POTATO_EMOTES)
        await msg.chat.send_message(msg.room, f"{emote} 🥔💥💣 @{ban_user} 🥔💥💣 YER BANNED")
        await twitch_instance.ban_user(streamer_id, streamer_id, tracker.get_user_id(ban_user), 'Lost at Hot Potato', settings.TIMEOUT_DURATION * 60)
        print(f"Timed out {ban_user}")

# this will be called whenever the !kiss command is issued
async def kiss(cmd: ChatCommand):
    default_names = ["Loose_Caboose", "xaddy_", "ubaru", "vori", "widejuicy", "djkumboi", "illicxt_bamb", "teaghandi"]
    kissed_user = random.choice(default_names)
    users = tracker.get_top_users()
    msg = random.choice(settings.KISS_MESSAGES)
    if (len(users) > len(default_names)):
        kissed_user = random.choice(users)
    msg = msg.replace('{x}', cmd.user.name).replace('{y}', kissed_user)
    await cmd.send(msg)
   
async def bot():
    global streamer_id, chat_instance, twitch_instance
    # setting up Authentication and getting your user id
    twitch = await Twitch(BOT_APP_ID, BOT_APP_SECRET)
    auth = UserAuthenticator(twitch, CHAT_SCOPE, force_verify=False)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, CHAT_SCOPE, refresh_token)

    pub = await Twitch(APP_ID, APP_SECRET)
    pub_auth = UserAuthenticator(pub, USER_SCOPE, force_verify=False)
    pub_token, pub_refresh_token = await pub_auth.authenticate()
    await pub.set_user_authentication(pub_token, USER_SCOPE, pub_refresh_token)

    user = await first(pub.get_users(logins=[TARGET_CHANNEL]))
    streamer_id = user.id
    twitch_instance = twitch

    # starting up chat
    chat = await Chat(twitch)
    chat_instance = chat
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_command('kiss', kiss)
    chat.start()

    # starting up PubSub
    pubsub = PubSub(pub)
    pubsub.start()

    uuid = await pubsub.listen_channel_points(user.id, callback_redemptions)
    
    # user input to stop the bot
    print('Enter S to stop bot')
    bot_active = True
    while bot_active:
        user_input = input()
        if user_input.lower() == 's':
            bot_active = False

    await pubsub.unlisten(uuid)
    pubsub.stop()
    chat.stop()
    await twitch.close()

asyncio.run(bot())
