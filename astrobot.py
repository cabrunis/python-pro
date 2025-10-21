import discord
from discord.ext import commands
import os
import json
import asyncio
import subprocess
import random
import platform
import psutil
from dotenv import load_dotenv
import ollama
from gtts import gTTS

# =========================
# 🔹 CARGAR VARIABLES DE ENTORNO
# =========================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# 🔹 CONFIGURACIÓN DEL BOT
# =========================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="%", intents=intents, help_command=None)  # 👈 Desactiva el help por defecto

# =========================
# 🔹 ASEGURAR ARCHIVOS
# =========================
def ensure_files():
    required_files = ["xp_data.json", "astro_log.txt"]
    for file in required_files:
        if not os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f:
                if file.endswith(".json"):
                    json.dump({}, f)
                else:
                    f.write("=== LOG INICIAL ===\n")
ensure_files()

# =========================
# 🔹 CARGAR / GUARDAR XP
# =========================
def cargar_xp():
    with open("xp_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_xp(data):
    with open("xp_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def asegurar_datos_usuario(user_id):
    data = cargar_xp()
    if user_id not in data:
        data[user_id] = {"xp": 0, "nivel": 1}
        guardar_xp(data)
    return data[user_id]

# =========================
# 🔹 EVENTOS
# =========================
@bot.event
async def on_ready():
    print(f"✅ {bot.user} conectado — Versión: Astro 5.0 Flash Galactic Ultimate+++ Edition")
    await bot.change_presence(
        activity=discord.Game("⚡ Astro 5.0 Flash Galactic Ultimate+++ Edition — %ayuda")
    )

# =========================
# 🔹 COMANDO AYUDA
# =========================
@bot.command(name="ayuda", aliases=["comandos"])
async def ayuda(ctx):
    # Embed principal
    embed = discord.Embed(
        title="🌠 Comandos disponibles",
        description="Estos son los comandos normales de **Astro 5.0 Flash Galactic Ultimate+++ Edition**",
        color=discord.Color.blue()
    )
    embed.add_field(name="%astro", value="Habla con la IA estelar (Ollama)", inline=False)
    embed.add_field(name="%xp", value="Muestra tu experiencia y nivel actual.", inline=False)
    embed.add_field(name="%ping", value="Muestra la latencia del bot.", inline=False)
    embed.add_field(name="%reiniciar", value="Reinicia el bot (modo galáctico).", inline=False)
    embed.set_footer(text="Versión: Astro 5.0 Flash Galactic Ultimate+++ Edition")

    # Embed de comandos secretos
    secretos = discord.Embed(
        title="🚀 Comandos Secretos de Astro",
        description="✨ No todos los héroes usan prefijos visibles...",
        color=discord.Color.purple()
    )
    secretos.add_field(name="%matrix", value="Desata el código binario de la galaxia.", inline=False)
    secretos.add_field(name="%sistema", value="Muestra información del sistema estelar.", inline=False)
    secretos.add_field(name="%energia", value="Calcula la energía vital de Astro.", inline=False)
    secretos.set_image(url=random.choice([
        "https://media.tenor.com/J2E-vLtiAsoAAAAd/ps5-ps5controller.gif",
        "https://media.tenor.com/AmhYb2aOWfEAAAAd/playstation-ps5.gif",
        "https://media.tenor.com/7XIzRa2ZfBoAAAAd/ps5-startup.gif"
    ]))
    secretos.set_footer(text="Versión: Astro 5.0 Flash Galactic Ultimate+++ Edition")

    await ctx.send(embed=embed)
    await asyncio.sleep(1)
    await ctx.send(embed=secretos)

@bot.command(name="astro-voz")
async def astro_voz(ctx, *, pregunta: str):
    """
    Responde usando Mistral y envía la respuesta en audio con gTTS.
    """
    # Generar la respuesta de Mistral
    respuesta = await respuesta(pregunta)

    # Crear archivo de audio con gTTS
    tts = gTTS(respuesta, lang='es')  # puedes cambiar 'es' por 'en' si quieres inglés
    archivo_audio = "respuesta.mp3"
    tts.save(archivo_audio)

    # Enviar el archivo al canal
    await ctx.send(f"🎙️ Respuesta de Mistral en audio para: {pregunta}")
    await ctx.send(file=discord.File(archivo_audio))

    # Limpiar el archivo después de enviarlo
    os.remove(archivo_audio)

# =========================
# 🔹 COMANDO ASTRO
# =========================
@bot.command()
async def astro(ctx, *, pregunta: str):
    user_id = str(ctx.author.id)
    asegurar_datos_usuario(user_id)

    try:
        respuesta = ollama.chat(model="mistral", messages=[{"role": "user", "content": pregunta}])
        texto = respuesta["message"]["content"]
    except Exception as e:
        texto = f"⚠️ Error con Ollama: {e}\nIntentando TinyLlama..."
        try:
            respuesta = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": pregunta}])
            texto = respuesta["message"]["content"]
        except Exception as e2:
            texto += f"\n❌ TinyLlama también falló. Reiniciando proceso..."
            await reiniciar(ctx)

    embed = discord.Embed(
        title="🧠 Respuesta Estelar",
        description=texto,
        color=discord.Color.green()
    )
    embed.set_footer(text="Versión: Astro 5.0 Flash Galactic Ultimate+++ Edition")
    await ctx.reply(embed=embed)

# =========================
# 🔹 OTROS COMANDOS
# =========================
@bot.command()
async def xp(ctx):
    data = cargar_xp()
    user_id = str(ctx.author.id)
    user_data = data.get(user_id, {"xp": 0, "nivel": 1})

    embed = discord.Embed(
        title=f"🌟 XP de {ctx.author.name}",
        description=f"Nivel: **{user_data['nivel']}**\nXP: **{user_data['xp']}**",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Versión: Astro 5.0 Flash Galactic Ultimate+++ Edition")
    await ctx.reply(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latencia: {round(bot.latency * 1000)} ms")

@bot.command()
async def reiniciar(ctx):
    await ctx.send("♻️ Reinicio galáctico en proceso...")
    await asyncio.sleep(2)
    os.system(f"{platform.python_executable} {__file__}")
    os._exit(0)

# =========================
# 🔹 COMANDOS SECRETOS
# =========================
@bot.command()
async def matrix(ctx):
    codigo = "".join(random.choice("01") for _ in range(256))
    await ctx.send(f"```{codigo}```")

@bot.command()
async def sistema(ctx):
    info = f"""
🖥️ Sistema: {platform.system()} {platform.release()}
⚙️ Procesador: {platform.processor()}
💾 RAM usada: {psutil.virtual_memory().percent}%
🔋 Carga CPU: {psutil.cpu_percent()}%
"""
    embed = discord.Embed(
        title="🛰️ Información del Sistema Estelar",
        description=info,
        color=discord.Color.teal()
    )
    embed.set_footer(text="Versión: Astro 5.0 Flash Galactic Ultimate+++ Edition")
    await ctx.send(embed=embed)

@bot.command()
async def energia(ctx):
    energia = random.randint(1, 100)
    await ctx.send(f"⚡ Nivel de energía galáctica de Astro: **{energia}%**")

# =========================
# 🔹 EJECUCIÓN DEL BOT
# =========================
if not TOKEN:
    raise ValueError("⚠️ No se encontró el token en el archivo .env (clave: DISCORD_TOKEN)")

bot.run(TOKEN)
