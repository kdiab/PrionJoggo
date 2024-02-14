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
#import config 
import dev as config
import settings

APP_ID = config.APP_ID
APP_SECRET = config.APP_SECRET
BOT_APP_ID = config.BOT_APP_ID
BOT_APP_SECRET = config.BOT_APP_SECRET
CHAT_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS]
TARGET_CHANNEL = config.TARGET_CHANNEL

# Initialize the tracker
tracker = ActiveUserTracker()

async def callback_redemptions(uuid: UUID, data: dict) -> None:
    display_name = data['data']['redemption']['user']['display_name']
    hot_potato = data['data']['redemption']['reward']['title']
    print(display_name, 'redeemed', hot_potato)

async def on_ready(ready_event: EventData):
    print('Ready to throw potatoes')
    await ready_event.chat.join_room(TARGET_CHANNEL)

async def reply(cmd: ChatCommand):
    await cmd.send('nice')

async def on_message(msg: ChatMessage):
    tracker.update_activity(msg.user.name, int(time.time()))
    if (msg.text.lower().startswith('@'+settings.BOT_NAME)):
        reply() 

# this will be called whenever the !reply command is issued
async def kiss(cmd: ChatCommand):
    default_names = [
    "Loose_Caboose", "SirMoses", "BossLofton", "Jonak", "LastSonido",
    "Sonic_KP3", "Faberator", "Unanemus", "Ivan", "BEHEMETH",
    "Georgepetervo", "SoloConway", "Xaddy", "Lusky", "Sainttits", "RyanIV",
    "mynamemikew", "DD214pls", "K1lla__Noob", "FluffyPigs", "Angryturkey546",
    "Dab_saget", "BioRome"
]
    kissed_user = random.choice(default_names)
    users = tracker.get_top_users()
    msg = random.choice(settings.KISS_MESSAGES)
    if (len(users) > len(default_names)):
        kissed_user = random.choice(users)
    msg = msg.replace('{x}', cmd.user.name).replace('{y}', kissed_user)
    await cmd.send(msg)

async def bot():
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
    
    # starting up chat
    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_command('kiss', kiss)
    chat.register_command('reply', reply)
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
