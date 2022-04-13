from discord.ext import commands
from sdb_lib import Log, Config
from os import listdir


bot = commands.Bot(
    command_prefix = Config.prefix,
    case_insensitive = True,
    help_command = None
)


def load_exts():
    errors = 0

    for folder in listdir("./exts/"):
        if "." in folder:
            continue

        for ext in listdir(f"./exts/{folder}/"):
            if not ext.endswith(".py"):
                continue

            ext = ext.removesuffix(".py")

            try:
                bot.load_extension(f"exts.{folder}.{ext}")
                Log.info(f"Loaded '{ext}'")
            except Exception as exc:
                Log.error(f"Failed to load '{ext}':\n'{exc}'")
                errors += 1

    return errors


@bot.event
async def on_ready():
    Log.info(f"Registered {len(bot.application_commands)} slash commands")
    Log.info(f"{bot.user.name} ({bot.application_id}) online")


Log.info("Loading extensions...")
errors = load_exts()
if errors > 0:
    Log.warning(f"{errors} error(s) while loading")

bot.run(Config.token)
