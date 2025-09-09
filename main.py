import os
import discord
from discord.ext import commands
from groq import AsyncGroq
from flask import Flask
import threading

# ---- Keep Alive Webserver ----
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

# ---- CONFIG ----
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MOD_ROLE_ID = 1262944317459267718

client = AsyncGroq(api_key=GROQ_API_KEY)

# ---- BASE CONSTANTS (TABLE VALUES) ----
TABLE_VALUES = {
    "gameid": 79976380444421,
    "isVerified": False,
    "custommapid": None,
    "gameversion": 0,
    "maxplayers": 50,
    "webhook": "",
    "whitelist": False,
    "Looting": 0,
}

# ---- DISCORD SETUP ----
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready for `.format` commands.")

# ---- AI CORRECTION ----
async def ai_correct_format(raw_text: str) -> str:
    prompt = f"""
You are a Roblox server config formatter.
Convert the following into the strict RoleplayM format.

Always enforce these table values:
{TABLE_VALUES}

Always:
- Capitalize server name words (except 'RP' which must be all caps).
- Use rbxassetid:// for iconid.
- Put correct group IDs in their fields.
- Leave webhook as "".
- If values are missing, use defaults from Table Values.

RoleplayM format:
["Server Name"] = {{
    -- MAIN
    gameid = 79976380444421,
    iconid = "rbxassetid://",
    maxplayers = 50,
    isVerified = false,
    description = "",
    whitelist = false,
    groupwhitelistid = 0,
    groupranktojoin = 0,
    microphoneonly = false,
    pvpserver = true,
    song = nil,
    songspeed = 1,
    gamepasses = {{ ["Looting"] = 0 }},
    background = nil,
    custommapid = nil,
    maskedservername = nil,
    bleeding = true,
    climbing = true,
    jumping = true,
    gameversion = 0,
    webhook = "",
    -- PERMISSIONS
    admingroup = 14628051,
    ranks = {{
        Owner = 255,
        CoOwner = 0,
        Headadmins = 0,
        Admins = 0,
        Moderator = 0
    }},
    ranktospawnguns = 0,
    ranktospawners = 0,
    ranktoshutdown = 0,
    pdgroup = 0;
}},

Now convert this:

{raw_text}
    """

    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

# ---- COMMAND ----
@bot.command()
async def format(ctx: commands.Context):
    if not ctx.message.reference:
        return await ctx.send("⚠️ Reply to a player's application with `.format`.")

    role = discord.utils.get(ctx.guild.roles, id=MOD_ROLE_ID)
    if role not in ctx.author.roles:
        return await ctx.send("❌ You don't have permission to use this.")

    replied_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    raw_text = replied_msg.content

    try:
        await ctx.message.delete()
    except:
        pass

    placeholder = await ctx.send("⏳ Formatting... please wait")

    try:
        corrected = await ai_correct_format(raw_text)
        await placeholder.edit(content=f"✅ Converted format:\n```lua\n{corrected}\n```")
    except Exception as e:
        await placeholder.edit(content="❌ Failed to process the format. Please try again.")

# ---- START BOT ----
if __name__ == "__main__":
    keep_alive()
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
