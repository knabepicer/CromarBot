import discord
import csv
import re
import random
from discord.ext import commands



bot = discord.Bot()


#bob = bot.create_group("bob", "Get Bells of Byelen data")
cromar = bot.create_group("cromar", "Get info about Cromar Bot")

test_ids = [1039354532167176303]
public_test_ids = [1039354532167176303,1081749141480288256]

@cromar.command(description="Get information about Cromar Bot.") # this decorator makes a slash command
async def help(ctx): 
    unitembed=discord.Embed(title="Available commands", color=0x676b68)
    unitembed.add_field(name='/bob unit [name]', value="Get Bells of Byelen unit data", inline=False)
    unitembed.add_field(name='/bob item [name]', value="Get Bells of Byelen item data", inline=False)
    unitembed.add_field(name='/bob skill [name]', value="Get Bells of Byelen skill data", inline=False)
    unitembed.add_field(name='/cota unit [name]', value="Get Call of the Armor unit data", inline=False)
    unitembed.add_field(name='/7s unit [name]', value="Get Seven Siblings unit data", inline=False)
    await ctx.response.send_message(embed=unitembed)

@cromar.command(guild_ids=test_ids)
async def numserver(ctx):
    servers = ""
    guilds = await bot.fetch_guilds(limit=150).flatten()
    for guild in guilds:
        servers += guild.name + '\n'
    await ctx.response.send_message(servers)

bot.load_extension("bob.bob")
bot.load_extension("cota.cota")
bot.load_extension("7s.sevens")
@bot.event
async def on_ready():
    
    print("Ready!")

token = ''
with open('token.txt') as f:
    token = f.read()

bot.run(token)