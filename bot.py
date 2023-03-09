import discord
import csv
import re
import random
import Cota.cota
import tlp.tlp
import sevensibs.sevens
from discord.ext import commands
from discord import option
import sys

bot = discord.Bot()

cromar = bot.create_group("cromar", "Use Cromar Bot commands")
#cota = cromar.create_subgroup("cota", "Get Call of the Armor data")

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
    unitembed.add_field(name='/trtr unit [name]', value="Get The Road to Ruin unit data", inline=False)
    unitembed.add_field(name='/tlp unit [name]', value="Get The Last Promise unit data", inline=False)
    unitembed.add_field(name='/tlp boss [name]', value="Get The Last Promise boss data", inline=False)
    await ctx.response.send_message(embed=unitembed)

@bot.slash_command(description = "Get playable unit data", guild_ids=public_test_ids)
@option("hack", description = "Name of the hack to get data for")
@option("name", description = "Name of the character to get data for")
async def unit(ctx, hack: str, name: str):
    if (hack == 'cota'):
        await Cota.cota.unit(ctx, name)
    elif (hack == 'tlp'):
        await tlp.tlp.unit(ctx, name)
    elif (hack == 'tlp'):
        await sevensibs.sevens.unit(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")

@bot.slash_command(description = "Get boss unit data", guild_ids=public_test_ids)
@option("hack", description = "Name of the hack to get data for")
@option("name", description = "Name of the character to get data for")
async def boss(ctx, hack: str, name: str):
    if (hack == 'tlp'):
        await tlp.tlp.boss(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")

bot.load_extension("bob.bob")
#bot.load_extension("cota.cota")
bot.load_extension("7s.sevens")
bot.load_extension("trtr.trtr")
#bot.load_extension("tlp.tlp")
@bot.event
async def on_ready():
    modulenames = set(sys.modules) & set(globals())
    allmodules = [sys.modules[name] for name in modulenames]
    for i in allmodules: print (' {}\n'.format(i))
    print("Ready!")
    print(dir(Cota))

token = ''
with open('token.txt') as f:
    token = f.read()

bot.run(token)