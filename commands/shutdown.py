import hikari as Hikari
import tanjun as Tanjun
import lavasnek_rs as Lavasnek
import sys

async def _leave_voice(ctx: Tanjun.abc.Context, lavalink: Lavasnek.Lavalink) -> None:
    assert ctx.guild_id is not None

    if lavalink.get_guild_gateway_connection_info(ctx.guild_id):
        await lavalink.destroy(ctx.guild_id)

        if ctx.client.shards:
            await ctx.client.shards.update_voice_state(ctx.guild_id, None)
            await lavalink.wait_for_connection_info_remove(ctx.guild_id)

        await lavalink.remove_guild_node(ctx.guild_id)
        await lavalink.remove_guild_from_loops(ctx.guild_id)
        return

    return

async def shutdown(ctx: Tanjun.abc.SlashContext, lavalink: Lavasnek.Lavalink = Tanjun.injected(type=Lavasnek.Lavalink)) -> None:
    if ctx.author.id != 332842719250481182:
        await ctx.respond('lol no only i can do that -ben', flags=Hikari.MessageFlag.EPHEMERAL)
        return
    
    await ctx.create_initial_response("Shutting down...")
    await _leave_voice(ctx, lavalink)
    await ctx.edit_initial_response("Bot is off.")
    await sys.exit(0)

shutdown_cmd = Tanjun.SlashCommand(
    shutdown,
    'shutdown',
    'Shuts the bot down. only i can do it btw',
)

component = Tanjun.Component().load_from_scope().make_loader()