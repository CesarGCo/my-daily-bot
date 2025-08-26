import os
import discord
from discord.ext import tasks, commands
import datetime
import pytz

# Token via variável de ambiente
TOKEN = os.getenv("DISCORD_TOKEN")
CANAL_ID = int(os.getenv("CHANNEL_ID", "0"))  # coloque o ID do canal no Render depois

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def eh_dia_de_daily():
    hoje = datetime.datetime.now(pytz.timezone("America/Sao_Paulo")).weekday()
    # segunda=0, terça=1, quarta=2, quinta=3, sexta=4
    return hoje in [1, 2, 4]  # terça, quarta e sexta

@tasks.loop(minutes=1)
async def daily_task():
    tz = pytz.timezone("America/Sao_Paulo")
    agora = datetime.datetime.now(tz).strftime("%H:%M")
    if agora == "21:00" and eh_dia_de_daily():
        canal = bot.get_channel(CANAL_ID)
        if canal:
            await canal.send(
                "@everyone 🚀 Bora pro daily!\n\n"
                "1️⃣ O que foi feito hoje?\n"
                "2️⃣ O que será feito amanhã?\n"
                "3️⃣ Existe algum impedimento?"
            )

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    daily_task.start()

bot.run(TOKEN)
