import random
import tanjun as Tanjun

async def roll(ctx: Tanjun.abc.SlashContext, dice: str) -> None:
    n = dice.find('d')
    d_amount = int(dice[:n])
    d_face = int(dice[n+1:])

    rolls = []

    for _ in range(d_amount):
        roll = random.randint(0, d_face)
        rolls.append(roll)

    await ctx.respond(f"{rolls}")

roll_cmd = Tanjun.SlashCommand(
    roll,
    'roll',
    'Rolls the dice. Defaults to 1d20.',
)

roll_cmd.add_str_option('dice', 'The type of dice to roll.', default='1d20')

component = Tanjun.Component().load_from_scope().make_loader()