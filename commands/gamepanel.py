import asyncio
from datetime import datetime
import hikari as Hikari
import tanjun as Tanjun
import yuyo as Yuyo

async def campaign_manager(ctx: Tanjun.abc.Context, component_client: Yuyo.ComponentClient = Tanjun.injected(type=Yuyo.ComponentClient)) -> None:
    row = (
        ctx.rest.build_action_row()
        .add_button(Hikari.ButtonStyle.PRIMARY, 'primary_button')
        .set_label("Primary button")
        .add_to_container()
        .add_button(Hikari.ButtonStyle.SECONDARY, 'secondary_button')
        .set_label("Secondary button")
        .add_to_container()
    )

    message = await ctx.respond(
        "Yuyo component test",
        component=row,
        ensure_result=True
    )

    executor = Yuyo.components.WaitFor(authors=(ctx.author.id,), timeout=datetime.timedelta(seconds=30))
    component_client.set_executor(message.id, executor)

    try:
        result = await executor.wait_for()
        msg_id = result.interaction.custom_id
    except asyncio.TimeoutError:
        await ctx.respond("Timeout 30000ms")
    else:
        await result.respond(f"Interaction ID: {msg_id}")

campaign_cmd = Tanjun.SlashCommand(
    campaign_manager,
    'campaign',
    'a',
)

component = Tanjun.Component().load_from_scope().make_loader()