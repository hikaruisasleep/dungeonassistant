import random
import hikari as Hikari
import tanjun as Tanjun

async def roll(ctx: Tanjun.abc.SlashContext, dice: str) -> None:
    n = dice.find('d')
    d_amount = int(dice[:n])
    d_face = int(dice[n+1:])

    ALLOWED_FACES = [4, 6, 8, 10, 12, 20, 100]

    if d_face not in ALLOWED_FACES:
        message = Hikari.Embed(title=f"❗ Wrong dice face!", color=Hikari.Color(0x3539BD)).add_field('Allowed dices', f"{Hikari.Emoji.parse('<:dice:948933152334819379>')} d4, d6, d8, d10, d12, d20, d100")
        await ctx.respond(embed=message)
        return

    rolls = []

    if d_face != 100:
        for _ in range(d_amount):
            roll = random.randint(1, d_face)
            rolls.append(roll)
    else:
        for _ in range(d_amount):
            rolltens = random.randint(0, 9)
            rollones = random.randint(0, 9)
            if rolltens > 0:
                roll = int(str(rolltens)+str(rollones))
            else:
                roll = rollones
            rolls.append(roll)

    nick = ctx.cache.get_member(ctx.get_guild(), ctx.author)
    if nick is None:
        nick = ctx.author.username
    else:
        nick = nick.nickname

    message = Hikari.Embed(title=f"{Hikari.Emoji.parse('<:dice:948933152334819379>')} {nick}'s {dice} roll", description=f'{rolls}', color=Hikari.Color(0x3539BD))

    await ctx.respond(embed=message, ensure_result=True)

roll_cmd = Tanjun.SlashCommand(
    roll,
    'roll',
    'Rolls the dice. Defaults to 1d20.',
)

roll_cmd.add_str_option('dice', 'The type of dice to roll.', default='1d20')

component = Tanjun.Component().load_from_scope().make_loader()