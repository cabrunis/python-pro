# 🎮 AstroBot 5.0 Flash Galactic Ultimate+++ Edition
# Confirmado por el Profesor Jirafales y el Sr. Barriga 😄
# Bot épico con IA local, XP, audio TTS, reinicio galáctico y mucho más

import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
import json
import sys
from dotenv import load_dotenv
from gtts import gTTS
import ollama
import subprocess
from datetime import datetime

# =========================
# CONFIGURACIÓN INICIAL
# =========================

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="%", intents=intents)

# =========================
# VARIABLES Y RUTAS
# =========================

XP_FILE = "xp_data.json"
AUDIO_DIR = "Astro_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

VERSION = "Astro 5.0 Flash Galactic Ultimate+++ Edition"
respuesta_count = 0
audio_count = 0

# Lista de juegos (50)
JUEGOS = [
    "Spider-Man 2", "Ratchet & Clank: Rift Apart", "Demon’s Souls", "Returnal", "God of War Ragnarök",
    "Horizon Forbidden West", "Gran Turismo 7", "Final Fantasy VII Rebirth", "Ghost of Tsushima",
    "Bloodborne", "Astro’s Playroom", "The Last of Us Part I", "Uncharted: Legacy of Thieves",
    "Sackboy: A Big Adventure", "Kena: Bridge of Spirits", "Forspoken", "Death Stranding: Director’s Cut",
    "Resident Evil 4 Remake", "Elden Ring", "Mortal Kombat 1", "Tekken 8", "Street Fighter 6",
    "Marvel’s Wolverine", "Silent Hill 2 Remake", "Until Dawn", "Days Gone", "Nioh 2", "Cyberpunk 2077",
    "Assassin’s Creed Mirage", "Lies of P", "Alan Wake 2", "Call of Duty: Modern Warfare III",
    "Baldur’s Gate 3", "Star Wars Jedi: Survivor", "The Witcher 3", "Persona 5 Royal", "Red Dead Redemption 2",
    "GTA V", "Final Fantasy XVI", "No Man’s Sky", "Resident Evil Village", "Dragon’s Dogma 2",
    "Helldivers 2", "Stellar Blade", "Pragmata", "Little Devil Inside", "Pacific Drive",
    "Project Eve", "Blue Protocol", "Ghostrunner 2", "Control 2", "Astro Bot: Rescue Mission 2"
]

# =========================
# FUNCIONES DE XP Y DATOS
# =========================

def ensure_xp_file_exists():
    if not os.path.exists(XP_FILE):
        with open(XP_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def cargar_xp():
    ensure_xp_file_exists()
    with open(XP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_xp(data):
    with open(XP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def asegurar_datos_usuario(usuario):
    data = cargar_xp()
    if usuario not in data:
        data[usuario] = {"xp": 0, "nivel": 1, "rebirths": 0}
        guardar_xp(data)

def ganar_xp(usuario, cantidad):
    data = cargar_xp()
    asegurar_datos_usuario(usuario)
    data[usuario]["xp"] += cantidad
    xp = data[usuario]["xp"]
    nivel = data[usuario]["nivel"]
    rebirths = data[usuario]["rebirths"]

    # Nivel máximo por rebirth
    if xp >= nivel * 100:
        data[usuario]["nivel"] += 1
        data[usuario]["xp"] = 0
        nivel = data[usuario]["nivel"]

        if nivel >= 10:
            if rebirths < 10:
                data[usuario]["nivel"] = 1
                data[usuario]["rebirths"] += 1
                rebirths = data[usuario]["rebirths"]
                guardar_xp(data)
                return f"🎉 ¡Felicidades! Alcanzaste el nivel 10 y renaciste (Rebirth {rebirths}/10). ¡Sigue brillando, jugador estelar! ✨"
            else:
                guardar_xp(data)
                return "🌟 ¡Has alcanzado el máximo poder (Rebirth 10)! No hay límites para ti, maestro galáctico."
        guardar_xp(data)
        return f"⬆️ Subiste al nivel {nivel}."
    guardar_xp(data)
    return None

# =========================
# CAMBIO DE ESTADO
# =========================

@tasks.loop(seconds=15)
async def cambiar_estado():
    juego = random.choice(JUEGOS)
    await bot.change_presence(activity=discord.Game(name=f"🎮 {juego}"))

# =========================
# AUTO-REINICIO GALÁCTICO
# =========================

async def reinicio_galactico():
    try:
        embed = discord.Embed(
            title="🪐 Reinicio Galáctico",
            description="Astro detectó un fallo grave o caída de modelo. Reiniciando el universo...",
            color=discord.Color.orange(),
        )
        embed.set_footer(text=VERSION)
        canal = discord.utils.get(bot.get_all_channels(), name="general")
        if canal:
            await canal.send(embed=embed)
    except:
        pass
    os.execv(sys.executable, ['python'] + sys.argv)

# =========================
# RESPUESTA CON IA LOCAL
# =========================

async def obtener_respuesta(prompt_usuario):
    prompt = f"Eres Astro, un robot amistoso experto en cualquier tema sobre PlayStation aunque también responderás otras cosas y hablarás completamente en español, simula que estas en 2025 y siempre se gracioso y amigable y si puedes manda alguno que otro emoji e intenta hacer referencias de Don Ramon. La pregunta es: {prompt_usuario}"
    try:
        respuesta = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return respuesta['message']['content']
    except Exception:
        try:
            respuesta = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": prompt}])
            return respuesta['message']['content']
        except Exception:
            await reinicio_galactico()

# =========================
# COMANDO PRINCIPAL ASTRO
# =========================

@bot.command(name="astro")
async def astro(ctx, *, pregunta: str):
    global respuesta_count, audio_count
    await ctx.typing()
    respuesta = await obtener_respuesta(pregunta)

    if not respuesta:
        respuesta = "⚠️ Hubo un error procesando tu pregunta. Intentando reinicio galáctico..."
        await reinicio_galactico()

    embed = discord.Embed(
        title="💫 Astro responde:",
        description=respuesta,
        color=random.randint(0, 0xFFFFFF)
    )
    embed.set_image(url=random.choice([
        "https://media.tenor.com/1FPOZf1DgFIAAAAd/spiderman2.gif",
        "https://media.tenor.com/9lH1XPJxUAcAAAAC/ratchet-riftapart.gif",
        "https://media.tenor.com/NF6cbJcXj7MAAAAC/returnal-playstation.gif",
        "https://media.tenor.com/7vVa8jM1qsYAAAAd/godofwar-ragnarok.gif"
    ]))
    embed.set_footer(text=VERSION)
    await ctx.send(embed=embed)

    # Audio TTS
    audio_count += 1
    nombre_audio = f"{AUDIO_DIR}/Astro_respuesta{audio_count}.mp3"
    tts = gTTS(text=respuesta, lang="es")
    tts.save(nombre_audio)
    await ctx.send(file=discord.File(nombre_audio))

    # Ganar XP
    xp_ganada = random.randint(5, 15)
    mensaje_nivel = ganar_xp(str(ctx.author.id), xp_ganada)
    if mensaje_nivel:
        await ctx.send(mensaje_nivel)

    respuesta_count += 1

# =========================
# COMANDO PING
# =========================

@bot.command(name="ping")
async def ping(ctx):
    global respuesta_count, audio_count
    embed = discord.Embed(
        title="📡 Estado del Bot",
        description=f"✅ Ping: {round(bot.latency * 1000)} ms\n💬 Respuestas enviadas: {respuesta_count}\n🎧 Audios generados: {audio_count}",
        color=discord.Color.blurple()
    )
    embed.set_footer(text=VERSION)
    await ctx.send(embed=embed)

# =========================
# COMANDO HOLA
# =========================

@bot.command(name="hola")
async def hola(ctx):
    embed = discord.Embed(
        title="👋 ¡Hola!",
        description="¡Hola, soy Astro! 🤖✨ Soy un bot especializado en PlayStation, aunque también responderé sobre cualquier otro tema. ¿En qué puedo ayudarte hoy?",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url="https://media.tenor.com/xU4hphF3eMgAAAAd/astro-bot-ps5.gif")
    embed.set_footer(text=VERSION)
    await ctx.send(embed=embed)

# =========================
# COMANDO AYUDA
# =========================

@bot.command(name="ayuda", aliases=["comandos"])
async def ayuda(ctx):
    embed1 = discord.Embed(
        title="🌟 Comandos Normales",
        description="Lista de comandos disponibles para todos los usuarios.",
        color=discord.Color.green()
    )
    embed1.add_field(name="%astro [pregunta]", value="Hazle una pregunta a Astro.", inline=False)
    embed1.add_field(name="%ping", value="Muestra el ping y estadísticas del bot.", inline=False)
    embed1.add_field(name="%ayuda", value="Muestra esta lista de comandos.", inline=False)
    embed1.add_field(name="%hola", value="¡Un Saludito!", inline=False)
    embed1.set_footer(text=VERSION)

    embed2 = discord.Embed(
        title="🤫 Comandos Secretos",
        description="Algunos comandos ocultos del laboratorio PS Lab.",
        color=discord.Color.purple()
    )
    embed2.add_field(name="%reinicio", value="Reinicia el bot manualmente.", inline=False)
    embed2.add_field(name="%nivel", value="Consulta tu nivel y rebirths.", inline=False)
    embed2.add_field(name="%sorpresa", value="¡Astro tiene algo especial para ti!", inline=False)
    embed2.set_image(url="https://media.tenor.com/xU4hphF3eMgAAAAd/astro-bot-ps5.gif")
    embed2.set_footer(text=VERSION)

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)

# =========================
# COMANDO DE ENTRADA
# =========================

@bot.event
async def on_ready():
    print(f"✅ {bot.user} se ha conectado correctamente.")

    # Embed de conexión
    embed = discord.Embed(
        title="🚀 ¡Astro está en línea!",
        description=f"**Astro 5.0 Flash Galactic Ultimate+++ Edition** se ha conectado con éxito.\n\n🪐 Ahora disponible en **{len(bot.guilds)} servidores**.\n",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://media.tenor.com/EpY9eDJWQkEAAAAd/astro-bot-ps5.gif")
    embed.set_footer(text="Sistema en línea • Astro 5.0 Flash Galactic Ultimate+++ Edition")

    # Intentar mandar el mensaje en el primer canal de texto disponible de cada servidor
    for guild in bot.guilds:
        try:
            canal = next(
                (ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),
                None
            )
            if canal:
                await canal.send(embed=embed)
        except Exception as e:
            print(f"⚠️ No se pudo enviar mensaje en {guild.name}: {e}")

    # Mostrar en consola
    print(f"🌌 Astro conectado en {len(bot.guilds)} servidores.")

# =========================
# COMANDOS SECRETOS
# =========================

@bot.command(name="reinicio")
async def reinicio(ctx):
    await ctx.send("♻️ Reinicio galáctico manual activado, preparen motores...")
    await reinicio_galactico()

@bot.command(name="nivel")
async def nivel(ctx):
    data = cargar_xp()
    user = str(ctx.author.id)
    if user not in data:
        asegurar_datos_usuario(user)
    nivel = data[user]["nivel"]
    rebirths = data[user]["rebirths"]
    xp = data[user]["xp"]
    await ctx.send(f"🌠 Nivel: {nivel} | XP: {xp}/100 | Rebirths: {rebirths}/10")

@bot.command(name="sorpresa")
async def sorpresa(ctx):
    await ctx.send("🎁 ¡Sorpresa desbloqueada! Gracias por ser parte del laboratorio PS Lab 💙")

# =========================
# EVENTOS
# =========================

@bot.event
async def on_ready():
    cambiar_estado.start()
    print(f"✅ {bot.user} conectado correctamente, el prefijo es %astro y los comandos se ven con %ayuda 🎮🎮🕹️🕹️")
    canal = discord.utils.get(bot.get_all_channels(), name="general")
    if canal:
        await canal.send(f"🚀 **{VERSION}** ha iniciado su viaje galáctico.")

# =========================
# EJECUCIÓN DEL BOT
# =========================

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: No se encontró el token en .env")
        sys.exit()
    bot.run(TOKEN)
