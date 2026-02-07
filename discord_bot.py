import discord
from discord import app_commands
from discord.ext import commands
import datetime
import platform
import psutil
import os

# ============================
# CONFIGURACIÓN DEL BOT
# ============================
TOKEN = 'MTQ2OTU2MzM5ODI0ODQ2NDQ0Nw.GlAUsU.-fS9My96SLGMQHK3qICBAowK1IZ8DB2G_gMn4M'  # ⚠️ REEMPLAZA ESTO CON TU TOKEN
TOKEN = 'MTQ2OTU2MzM5ODI0ODQ2NDQ0Nw.GlAUsU.-fS9My96SLGMQHK3qICBAowK1IZ8DB2G_gMn4M'
# Intents necesarios para el bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Crear el bot
bot = commands.Bot(command_prefix='!', intents=intents)

# ============================
# EVENTO: Bot listo
# ============================
@bot.event
async def on_ready():
    """Se ejecuta cuando el bot se conecta exitosamente"""
    print(f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print(f'✅ Bot conectado como: {bot.user.name}')
    print(f'🆔 ID: {bot.user.id}')
    print(f'🌐 Servidores: {len(bot.guilds)}')
    print(f'👥 Usuarios: {len(bot.users)}')
    print(f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    
    # Sincronizar comandos slash
    try:
        synced = await bot.tree.sync()
        print(f'✨ {len(synced)} comandos sincronizados')
    except Exception as e:
        print(f'❌ Error al sincronizar comandos: {e}')
    
    # Establecer estado del bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="tu servidor | /info"
        ),
        status=discord.Status.online
    )

# ============================
# COMANDO: /info
# ============================
@bot.tree.command(name="info", description="Muestra información detallada del bot")
async def info_command(interaction: discord.Interaction):
    """Comando /info con información completa del bot"""
    
    # Calcular uptime
    uptime = datetime.datetime.now() - bot.start_time
    uptime_str = str(uptime).split('.')[0]
    
    # Uso de RAM
    process = psutil.Process(os.getpid())
    ram_usage = process.memory_info().rss / 1024 / 1024  # En MB
    
    # Latencia
    latency = round(bot.latency * 1000)
    
    # Crear embed elegante
    embed = discord.Embed(
        title="🤖 Información del Bot",
        description="Bot creado con Discord.py | Potenciado por Python 🐍",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    
    # Thumbnail (icono del bot)
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)
    
    # Información general
    embed.add_field(
        name="📊 Estadísticas",
        value=f"```\n"
              f"Servidores: {len(bot.guilds)}\n"
              f"Usuarios: {len(bot.users)}\n"
              f"Comandos: {len(bot.tree.get_commands())}\n"
              f"```",
        inline=True
    )
    
    # Rendimiento
    embed.add_field(
        name="⚡ Rendimiento",
        value=f"```\n"
              f"Ping: {latency}ms\n"
              f"RAM: {ram_usage:.1f} MB\n"
              f"Uptime: {uptime_str}\n"
              f"```",
        inline=True
    )
    
    # Sistema
    embed.add_field(
        name="🖥️ Sistema",
        value=f"```\n"
              f"Python: {platform.python_version()}\n"
              f"Discord.py: {discord.__version__}\n"
              f"OS: {platform.system()}\n"
              f"```",
        inline=True
    )
    
    # Creador
    embed.add_field(
        name="👨‍💻 Desarrollador",
        value="<@vladimirfernan>",
        inline=True
    )
    
    # Fecha de creación
    bot_created = bot.user.created_at.strftime("%d/%m/%Y")
    embed.add_field(
        name="📅 Fecha de Creación",
        value=f"`{bot_created}`",
        inline=True
    )
    
    # Links útiles
    embed.add_field(
        name="🔗 Enlaces",
        value="[Invitar Bot](https://discord.com/api/oauth2/authorize?client_id=TU_CLIENT_ID&permissions=8&scope=bot) | "
              "[Soporte](https://discord.gg/tu-servidor)",
        inline=True
    )
    
    # Footer
    embed.set_footer(
        text=f"Solicitado por {interaction.user.name}",
        icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
    )
    
    await interaction.response.send_message(embed=embed)

# ============================
# COMANDO: /ping
# ============================
@bot.tree.command(name="ping", description="Muestra la latencia del bot")
async def ping_command(interaction: discord.Interaction):
    """Comando simple para verificar la latencia"""
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latencia: **{latency}ms**",
        color=discord.Color.green() if latency < 100 else discord.Color.orange()
    )
    
    await interaction.response.send_message(embed=embed)

# ============================
# COMANDO: /serverinfo
# ============================
@bot.tree.command(name="serverinfo", description="Muestra información del servidor actual")
async def serverinfo_command(interaction: discord.Interaction):
    """Información detallada del servidor"""
    guild = interaction.guild
    
    # Contar tipos de canales
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    
    # Contar roles
    roles = len(guild.roles)
    
    # Nivel de verificación
    verification_levels = {
        discord.VerificationLevel.none: "Ninguno",
        discord.VerificationLevel.low: "Bajo",
        discord.VerificationLevel.medium: "Medio",
        discord.VerificationLevel.high: "Alto",
        discord.VerificationLevel.highest: "Muy Alto"
    }
    
    embed = discord.Embed(
        title=f"🏰 {guild.name}",
        description=guild.description if guild.description else "Sin descripción",
        color=discord.Color.purple(),
        timestamp=datetime.datetime.now()
    )
    
    # Icono del servidor
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    # Información básica
    embed.add_field(
        name="👑 Dueño",
        value=guild.owner.mention,
        inline=True
    )
    
    embed.add_field(
        name="🆔 ID del Servidor",
        value=f"`{guild.id}`",
        inline=True
    )
    
    embed.add_field(
        name="📅 Creado el",
        value=guild.created_at.strftime("%d/%m/%Y"),
        inline=True
    )
    
    # Miembros
    embed.add_field(
        name="👥 Miembros",
        value=f"```\nTotal: {guild.member_count}\n```",
        inline=True
    )
    
    # Canales
    embed.add_field(
        name="📺 Canales",
        value=f"```\nTexto: {text_channels}\nVoz: {voice_channels}\nCategorías: {categories}\n```",
        inline=True
    )
    
    # Roles
    embed.add_field(
        name="🎭 Roles",
        value=f"```\n{roles} roles\n```",
        inline=True
    )
    
    # Seguridad
    embed.add_field(
        name="🔒 Seguridad",
        value=f"Verificación: {verification_levels.get(guild.verification_level, 'Desconocido')}",
        inline=True
    )
    
    # Boost
    embed.add_field(
        name="✨ Nitro Boost",
        value=f"Nivel {guild.premium_tier} ({guild.premium_subscription_count} boosts)",
        inline=True
    )
    
    embed.set_footer(text=f"Solicitado por {interaction.user.name}")
    
    await interaction.response.send_message(embed=embed)

# ============================
# EVENTO: Mensaje de bienvenida
# ============================
@bot.event
async def on_member_join(member):
    """Se ejecuta cuando un nuevo miembro se une al servidor"""
    # Buscar canal de bienvenida (puedes cambiar el nombre)
    channel = discord.utils.get(member.guild.text_channels, name='bienvenida')
    
    if channel:
        embed = discord.Embed(
            title="👋 ¡Nuevo Miembro!",
            description=f"¡Bienvenido {member.mention} a **{member.guild.name}**!",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="📊 Miembro número", value=f"#{member.guild.member_count}", inline=True)
        embed.set_footer(text=f"ID: {member.id}")
        
        await channel.send(embed=embed)

# ============================
# MANEJO DE ERRORES
# ============================
@bot.event
async def on_command_error(ctx, error):
    """Manejo global de errores"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos para usar este comando.")
    else:
        print(f"Error: {error}")

# ============================
# INICIAR EL BOT
# ============================
if __name__ == "__main__":
    # Guardar tiempo de inicio
    bot.start_time = datetime.datetime.now()
    
    # Verificar que el token no sea el placeholder
    if TOKEN == 'TU_TOKEN_AQUI':
        print("❌ ERROR: Debes reemplazar 'TU_TOKEN_AQUI' con tu token real en la línea 13")
        print("💡 Obtén tu token en: https://discord.com/developers/applications")
    else:
        try:
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("❌ ERROR: Token inválido. Verifica que sea correcto.")
        except Exception as e:
            print(f"❌ ERROR al iniciar el bot: {e}")
