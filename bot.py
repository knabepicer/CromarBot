import discord
import csv
import re
import random
import Cota.cota
import tlp.tlp
import sevensibs.sevens
import bob.bob
import trtr.trtr
import vq.vq
import vba.vba
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
    unitembed.add_field(name="Hack Abbreviations", value="https://github.com/knabepicer/CromarBot/blob/main/Hack%20abbreviations.txt",inline=False)
    unitembed.add_field(name='/unit [hack] [name]', value="Get unit data - currently supports 7s, bob, cota, tlp, trtr, vq, vba", inline=False)
    unitembed.add_field(name='/item [hack] [name]', value="Get item data - currently supports bob", inline=False)
    unitembed.add_field(name='/skill [hack] [name]', value="Get skill data - currently supports bob", inline=False)
    unitembed.add_field(name='/boss [hack] [name]', value="Get boss data - currently supports tlp", inline=False)
    await ctx.response.send_message(embed=unitembed)

async def get_unit_names(ctx: discord.AutocompleteContext):
    hack = ctx.options['hack']
    if (hack == 'cota'):
        return Cota.cota.get_unit_names(ctx)
    elif (hack == 'tlp'):
        return tlp.tlp.get_unit_names(ctx)
    elif (hack == '7s'):
        return sevensibs.sevens.get_unit_names(ctx)
    elif (hack == 'bob'):
        return bob.bob.get_unit_names(ctx)
    elif (hack == 'trtr'):
        return trtr.trtr.get_unit_names(ctx)
    elif (hack == 'vq'):
        return vq.vq.get_unit_names(ctx)
    elif (hack == 'vba'):
        return vba.vba.get_unit_names(ctx)
    else:
        return []
    


@bot.slash_command(description = "Get playable unit data")
@option("hack", description = "Name of the hack to get data for",
        autocomplete=discord.utils.basic_autocomplete(
        ["cota", "tlp", "7s", "bob", 'trtr', 'vq']
    ))
@option("name", description = "Name of the character to get data for", autocomplete=get_unit_names)
async def unit(ctx, hack: str, name: str):
    if (hack == 'cota'):
        await Cota.cota.unit(ctx, name)
    elif (hack == 'tlp'):
        await tlp.tlp.unit(ctx, name)
    elif (hack == '7s'):
        await sevensibs.sevens.unit(ctx, name)
    elif (hack == 'bob'):
        await bob.bob.unit(ctx, name)
    elif (hack == 'trtr'):
        await trtr.trtr.unit(ctx, name)
    elif (hack == 'vq'):
        await vq.vq.unit(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")

@bot.slash_command(description = "Get boss unit data")
@option("hack", description = "Name of the hack to get data for",
        autocomplete=discord.utils.basic_autocomplete(
        ["tlp"]
    ))
@option("name", description = "Name of the character to get data for")
async def boss(ctx, hack: str, name: str):
    if (hack == 'tlp'):
        await tlp.tlp.boss(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")

@bot.slash_command(description = "Get item data")
@option("hack", description = "Name of the hack to get data for")
@option("name", description = "Name of the item to get data for",
        autocomplete=discord.utils.basic_autocomplete(
        ["bob"]
    ))
async def item(ctx, hack: str, name: str):
    if (hack == 'bob'):
        await bob.bob.item(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")

@bot.slash_command(description = "Get skill data")
@option("hack", description = "Name of the hack to get data for")
@option("name", description = "Name of the skill to get data for",
        autocomplete=discord.utils.basic_autocomplete(
        ["bob"]
    ))
async def skill(ctx, hack: str, name: str):
    if (hack == 'bob'):
        await bob.bob.skill(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")

#bot.load_extension("bob.bob")
#bot.load_extension("cota.cota")
#bot.load_extension("7s.sevens")
#bot.load_extension("trtr.trtr")
#bot.load_extension("tlp.tlp")
@bot.event
async def on_ready():
    
    print("Ready!")
   

token = ''
with open('token.txt') as f:
    token = f.read()

bot.run(token)