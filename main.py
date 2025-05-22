import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import webserver

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

#remember to enable intents if something isnt working
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

#decorator in python
@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

#send the member a welcome message
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

#just a random function
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    #allows bot to continue processing the rest of the commands
    await bot.process_commands(message)

@bot.command()
async def start_countdown(ctx):
    #begin countdown
    await ctx.send("💣 Countdown begins, explosion in:")
    #begin 10 second countdown
    for i in range(10, 0, -1):
        await ctx.send(f"{i}...")
        await asyncio.sleep(1)
    #explosion that disconnects everyone
    await ctx.send("💥 BOOM!")
    await disconnect_all(ctx)
    #dont let them join for 30 seconds because of radiation
    for i in range(30, 0, -1):
        await radiation(ctx)
        await asyncio.sleep(1)
                

    
#command to disconnect everyone in the server
@bot.command()
@commands.has_permissions(move_members=True)
async def disconnect_all(ctx):
    for member in ctx.guild.members:
        if member.voice and not member.bot:
            try:
                await member.move_to(None)  # Disconnects from voice
            except Exception as e:
                await ctx.send(f"Couldn't disconnect {member.name}: {e}")

#command to disconnect everyone because of radiation
@bot.command()
@commands.has_permissions(move_members=True)
async def radiation(ctx):
    for member in ctx.guild.members:
        if member.voice and not member.bot:
            try:
                await member.move_to(None)  # Disconnects from voice
                await ctx.send(f"{member.mention} there is radiation!!!")
            except Exception as e:
                await ctx.send(f"Couldn't disconnect {member.name}: {e}")

#just a quick little info command
@bot.command()
async def info(ctx):
    await ctx.send(f"Hello {ctx.author.mention}, I'm NukeBot.")
    await ctx.send("Im designed to nuke the server.")
    await ctx.send("I don't mean destroy it, I just mean")
    await ctx.send("kick everyone!")
    await ctx.send("But be careful, my powerful explosion")
    await ctx.send("leaves radiactive fallout!")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)

