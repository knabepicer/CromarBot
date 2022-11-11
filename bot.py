import discord
from discord import app_commands
from discord.ext import commands
import csv

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "bob", 
description = "Get Bells of Byelen data", 
)
 #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction: discord.Interaction, type: str, name: str):
    if (type == "unit"):
        with open('bob unit.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            was_found = False
            for row in reader:
                if(row['Name'].lower() == (name + "name")):
                    #await interaction.response.send_message("Name: " + row["Name"] + " HP Growth:" + row["HP Growth"])
                    unitembed=discord.Embed(title=name.capitalize(), color=0xac6c6c)
                    unitembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/995490005550121000/1040464509573267566/Cromarknabepicer.png")
                    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Support Class'], inline=False)
                    bases = "HP: " + row['HP'] + " | " + "Str:" + row['Atk'] + " | " + "Mag: value | Skl:" + row['Skl'] + " | " + "Spd:" + row['Spd'] + " | " + "Lck:" + row['Luck'] + " | " + "Def:" + row['Def'] + " | " + "Res:" + row['Res'] + " | " + "Bld:" + row['Con'] + " | " + "Mov: value"
                    unitembed.add_field(name="Bases", value=bases, inline=False)
                    growths = "HP:" + row['HP Growth'] + " | " + "Str:" + row['Atk Growth'] + " | " + "Mag: value | Skl:" + row['Skl Growth'] + " | " + "Spd:" + row['Spd Growth'] + " | " + "Lck:" + row['Luck Growth'] + " | " + "Def:" + row['Def Growth'] + " | " + "Res:" + row['Res Growth'] + " | " + "Bld: value | Mov: value"
                    unitembed.add_field(name="Growths", value=growths, inline=False)
                    await interaction.response.send_message(embed=unitembed)
                    was_found = True
            if (not was_found):
                await interaction.response.send_message("That unit does not exist.")
                
    elif (type == "item"):
        await interaction.response.send_message("You requested data for the item known as " + name)
    else:
        await interaction.response.send_message("Must either ask for a \'unit\' or an \'item\'")

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

token = 'MTAzOTM0MjA4MTI0NTcyNDcyMw.GRNUKI.mvXH25mYHEKqr_Q4SYYzRVyQUoxr2kOR8_0XjI'

client.run(token)