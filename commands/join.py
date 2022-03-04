import hikari as Hikari
import tanjun as Tanjun

async def join(ctx: Tanjun.abc.SlashContext) -> None:
    # get the voice channel
    states = ctx.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]

    # check if the author is in a voice channel
    if not voice_state:
        await ctx.respond('Channel not found')
        return

    # connect to the voice channel
    channel_id = voice_state[0].channel_id
    
    await ctx.respond(f"Connected to <#{channel_id}>")

join_cmd = Tanjun.SlashCommand(
    join,
    'join',
    'Joins the voice channel the user is currently in.',
)

component = Tanjun.Component().load_from_scope().make_loader()