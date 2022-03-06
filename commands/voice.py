import typing

import hikari as Hikari
import lavasnek_rs as Lavasnek
import tanjun as Tanjun

async def join_as_slash(ctx: Tanjun.abc.SlashContext, lavalink: Lavasnek.Lavalink = Tanjun.inject(type=Lavasnek.Lavalink),
) -> None:
    if channel := await _join_voice(ctx, lavalink):
        await ctx.respond(f"Connected to <#{channel}>")

async def _join_voice(ctx: Tanjun.abc.Context, lavalink: Lavasnek.Lavalink) -> typing.Optional[Hikari.Snowflake]:
    assert ctx.guild_id is not None

    if ctx.client.cache and ctx.client.shards:
        if (voice_state := ctx.client.cache.get_voice_state(ctx.guild_id, ctx.author)) is None:
            await ctx.respond("Please connect to a voice channel.")
            return None

        await ctx.client.shards.update_voice_state(ctx.guild_id, voice_state.channel_id, self_deaf=True)
        conn = await lavalink.wait_for_full_connection_info_insert(ctx.guild_id)
        await lavalink.create_session(conn)
        return voice_state.channel_id

    await ctx.respond("Unable to join voice. The cache is disabled or shards are down.")
    return None

join_cmd = Tanjun.SlashCommand(
    join_as_slash,
    'join',
    'Joins the voice channel you are currently in',
)

async def leave_as_slash(ctx: Tanjun.abc.SlashContext, lavalink: Lavasnek.Lavalink = Tanjun.inject(type=Lavasnek.Lavalink)) -> None:
    await _leave_voice(ctx, lavalink)

async def _leave_voice(ctx: Tanjun.abc.Context, lavalink: Lavasnek.Lavalink) -> None:
    assert ctx.guild_id is not None

    if lavalink.get_guild_gateway_connection_info(ctx.guild_id):
        await lavalink.destroy(ctx.guild_id)

        if ctx.client.shards:
            await ctx.client.shards.update_voice_state(ctx.guild_id, None)
            await lavalink.wait_for_connection_info_remove(ctx.guild_id)

        await lavalink.remove_guild_node(ctx.guild_id)
        await lavalink.remove_guild_from_loops(ctx.guild_id)
        await ctx.respond("Disconnected from voice.")
        return

    await ctx.respond("I am not currently connected.")

leave_cmd = Tanjun.SlashCommand(
    leave_as_slash,
    'leave',
    'Leaves the voice channel.',
)
dc_cmd = Tanjun.SlashCommand(
    leave_as_slash,
    'dc',
    'Leaves the voice channel.',
)

component = Tanjun.Component().load_from_scope().make_loader()
