import os
import hikari as Hikari
import tanjun as Tanjun
from dotenv import load_dotenv
load_dotenv()

def create_client(bot: Hikari.GatewayBot) -> Tanjun.Client:
    client = (Tanjun.Client.from_gateway_bot(bot, mention_prefix=True).add_prefix('0_'))
    return client

def create_bot() -> Hikari.GatewayBot:
    TOKEN = os.environ.get('TOKEN')
    bot = Hikari.GatewayBot(intents=Hikari.Intents.ALL_UNPRIVILEGED, token=TOKEN)

    create_client(bot)

    return bot
