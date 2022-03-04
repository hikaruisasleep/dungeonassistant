import os
import hikari as Hikari
import tanjun as Tanjun
import lavasnek_rs as Lavasnek
from dotenv import load_dotenv
load_dotenv()
import modules.voice as voice

TOKEN = os.environ.get('TOKEN')

GUILD_ID = os.environ.get('GUILD_ID')
DND_VOICE = os.environ.get('DND_VOICE')
DND_MAIN = os.environ.get('DND_MAIN')
OUTGAME = os.environ.get('OUTGAME')

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
    client = (Tanjun.Client.from_gateway_bot(bot, mention_prefix=True, declare_global_commands=775253878312009768).add_prefix('/'))
    module_loader(client, 'commands')
    return client

def create_bot():
    bot = Hikari.GatewayBot(intents=Hikari.Intents.ALL_UNPRIVILEGED, token=TOKEN)
    client = create_client(bot)
    return bot, client

bot, client = create_bot()

@client.with_listener(Hikari.ShardReadyEvent)
async def on_shard_ready(event: Hikari.ShardReadyEvent, client_: Tanjun.Client = Tanjun.injected(type=Tanjun.Client)) -> None:
    builder = (
        Lavasnek.LavalinkBuilder(event.my_user.id, TOKEN)
        .set_host("127.0.0.1")
        .set_password("youshallnotpass")
        .set_start_gateway(False)
    )

    client_.set_type_dependency(Lavasnek.Lavalink, await builder.build(voice.EventHandler))

@client.with_listener(Hikari.VoiceStateUpdateEvent)
async def on_voice_state_update(event: Hikari.VoiceStateUpdateEvent, lavalink: Lavasnek.Lavalink = Tanjun.injected(type=Lavasnek.Lavalink)) -> None:
    lavalink.raw_handle_event_voice_state_update(
        event.state.guild_id,
        event.state.user_id,
        event.state.session_id,
        event.state.channel_id,
    )

@client.with_listener(Hikari.VoiceServerUpdateEvent)
async def on_voice_server_update(event: Hikari.VoiceServerUpdateEvent, lavalink: Lavasnek.Lavalink = Tanjun.injected(type=Lavasnek.Lavalink)) -> None:
    if event.endpoint is not None:
        await lavalink.raw_handle_event_voice_server_update(
            event.guild_id,
            event.endpoint,
            event.token,
        )

bot.run(asyncio_debug=True, coroutine_tracking_depth=20)
