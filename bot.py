import os
import hikari as Hikari
import tanjun as Tanjun
import lavaplayer as LavaPlayer
from dotenv import load_dotenv
load_dotenv()
import modules.voice as voice

GUILD_ID:int = os.environ.get('GUILD_ID') | 775253878312009768
DND_VOICE:int = os.environ.get('DND_VOICE') | 948880697836322827
DND_MAIN:int = os.environ.get('DND_MAIN') | 948880372643549215
OUTGAME:int = os.environ.get('OUTGAME') | 948898663332196352

def module_loader(client: Tanjun.Client, path):
    modules = []
    for (_, _, files) in os.walk('./' + path):
        modules.extend(files)
        break
    for file in modules:
        if file.startswith('__'):
            modules.remove(file)
        else:
            i = file.find('.')
            modules[modules.index(file)] = file[:i]

    for module in modules:
        client.load_modules(path + '.' + module)

def create_client(bot: Hikari.GatewayBot) -> Tanjun.Client:
    client = (Tanjun.Client.from_gateway_bot(bot, mention_prefix=True, declare_global_commands=GUILD_ID).add_prefix('/'))
    module_loader(client, 'commands')
    return client

def create_bot() -> Hikari.GatewayBot:
    TOKEN = os.environ.get('TOKEN')
    bot = Hikari.GatewayBot(intents=Hikari.Intents.ALL_UNPRIVILEGED, token=TOKEN)

    create_client(bot)

    return bot

bot = create_bot()

@bot.listen(Hikari.StartedEvent)
async def started_event(event):
    voice.lavalink.connect()
    channel_id = DND_VOICE
    guild_id = GUILD_ID
    await bot.update_voice_state(guild_id, channel_id, self_deaf=False, self_mute=True)
@bot.listen(Hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: Hikari.VoiceStateUpdateEvent):
    await voice.lavalink.raw_voice_state_update(event.guild_id, event.state.user_id, event.state.session_id, event.state.channel_id)
@bot.listen(Hikari.VoiceServerUpdateEvent)
async def voice_server_update(event: Hikari.VoiceServerUpdateEvent):
    await voice.lavalink.raw_voice_server_update(event.guild_id, event.endpoint, event.token)

bot.run(asyncio_debug=True, coroutine_tracking_depth=20)
