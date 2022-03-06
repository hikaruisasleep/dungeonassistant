import hikari as Hikari
import tanjun as Tanjun
import yuyo as Yuyo

component = Tanjun.Component()

async def persistence_callback(ctx: Yuyo.ComponentContext):
    await ctx.respond(f'Pressed.')

@component.with_listener(Hikari.StartedEvent)
async def on_bot_ready(_: Hikari.StartedEvent, component_client: Yuyo.ComponentClient = Tanjun.inject(type=Yuyo.ComponentClient)):
    component_client.set_constant_id('primary-click', persistence_callback)

@component.with_command
@Tanjun.as_slash_command('campaign', 'Global campaign manager panel')
async def campaign_manager(ctx: Tanjun.abc.Context) -> None:
    row = (
        ctx.rest.build_action_row()
        .add_button(Hikari.ButtonStyle.PRIMARY, 'primary-click')
        .set_label("Primary button")
        .add_to_container()
    )

    await ctx.respond(
        "Yuyo component test",
        component=row
    )

@Tanjun.as_loader
def load(client: Tanjun.abc.Client) -> None:
    client.add_component(component.copy())
