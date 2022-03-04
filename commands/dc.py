import hikari as Hikari
import tanjun as Tanjun
import lavasnek_rs as Lavasnek
import sys

async def dc(ctx: Tanjun.abc.SlashContext) -> None:
    if ctx.author.id != 332842719250481182:
        await ctx.respond('lol no only i can do that -ben', flags=Hikari.MessageFlag.EPHEMERAL)
        return
    
    await ctx.create_initial_response("Shutting down...")
    await Tanjun.injected(type=Lavasnek.Lavalink).destroy(ctx.guild_id)
    await Tanjun.injected(type=Lavasnek.Lavalink).leave(ctx.guild_id)
    await ctx.client.close()

dc_cmd = Tanjun.SlashCommand(
    dc,
    'dc',
    'Shuts the bot down. only i can do it btw',
)

component = Tanjun.Component().load_from_scope().make_loader()