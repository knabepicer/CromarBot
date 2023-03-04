import discord
import csv
import re
import random
from discord.ext import commands



bot = discord.Bot()


#bob = bot.create_group("bob", "Get Bells of Byelen data")
cromar = bot.create_group("cromar", "Get info about Cromar Bot")

current_ids = [1039354532167176303, 828646591471550474, 1030675539314352252]

@cromar.command(description="Get information about Cromar Bot.") # this decorator makes a slash command
async def help(ctx): 
    unitembed=discord.Embed(title="Available commands", color=0x676b68)
    unitembed.add_field(name='/bob unit [name]', value="Get Bells of Byelen unit data", inline=False)
    unitembed.add_field(name='/bob item [name]', value="Get Bells of Byelen item data", inline=False)
    unitembed.add_field(name='/bob skill [name]', value="Get Bells of Byelen skill data", inline=False)
    unitembed.add_field(name='/cota unit [name]', value="Get Call of the Armor unit data", inline=False)
    await ctx.response.send_message(embed=unitembed)


 #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.

bot.load_extension("bob.bob")
bot.load_extension("cota.cota")
bot.load_extension("paginator")
@bot.event
async def on_ready():
    #await bot.load_extension("cota")
    
    print("Ready!")

token = ''
with open('token.txt') as f:
    token = f.read()

bot.run(token)