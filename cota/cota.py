import discord
import csv
import re
import random
from discord.ext import commands
from discord import option

class Cota(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cota = discord.SlashCommandGroup("cota", "Get Call of the Armor unit data")

    @cota.command(description = "Get Call of the Armor unit data")
    @option("name", description = "Name of the character to get data for")
    async def unit(self, ctx, name: str):
        stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
        with open('cota unit.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            was_found = False
            for row in reader:
                stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
                if(stripped_row.lower() == stripped_name.lower()):
                    unitembed=discord.Embed(title=row['Name'], color=0x47CAFF)
                    unitembed.set_thumbnail(url=row['Portrait'])
                    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
                    unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
                    bases = "HP " + row['HP'] + " | " + "Atk " + row['Atk'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
                    unitembed.add_field(name="Bases", value=bases, inline=False)
                    growths = "HP " + row['HP Growth'] + "% | " + "Atk " + row['Atk Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
                    unitembed.add_field(name="Growths", value=growths, inline=False)
                    ranks = cota_get_ranks(row)
                    unitembed.add_field(name="Ranks", value=ranks, inline=False)
                    if (row['Promotes'] == "Yes"):
                        gains = cota_get_gains(row)
                        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
                    await ctx.response.send_message(embed=unitembed)
                    was_found = True
            if (not was_found):
                await ctx.response.send_message("That unit does not exist.")


def cota_get_ranks(row):
    ranks = ""
    if (row['Sword'] != 'None'):
        ranks += "Sword: " + row['Sword'] + " | "
    if (row['Lance'] != 'None'):
        ranks += "Lance: " + row['Lance'] + " | "
    if (row['Axe'] != 'None'):
        ranks += "Axe: " + row['Axe'] + " | "
    if (row['Bow'] != 'None'):
        ranks += "Bow: " + row['Bow'] + " | "
    if (row['Staff'] != 'None'):
        ranks += "Staff: " + row['Staff'] + " | "
    if (row['Anima'] != 'None'):
        ranks += "Anima: " + row['Anima'] + " | "
    if (row['Light'] != 'None'):
        ranks += "Light: " + row['Light'] + " | "
    if (row['Dark'] != 'None'):
        ranks += "Dark: " + row['Dark'] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "None"
    return ranks

def cota_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != '0'):
        gains += "HP: +" + row['HP Gains'] + " | "
    if (row['Atk Gains'] != '0'):
        gains += "Atk: +" + row['Atk Gains'] + " | "
    if (row['Skl Gains'] != '0'):
        gains += "Skl: +" + row['Skl Gains'] + " | "
    if (row['Spd Gains'] != '0'):
        gains += "Spd: +" + row['Spd Gains'] + " | "
    if (row['Def Gains'] != '0'):
        gains += "Def: +" + row['Def Gains'] + " | "
    if (row['Res Gains'] != '0'):
        gains += "Res: +" + row['Res Gains'] + " | "
    if (row['Con Gains'] != '0'):
        gains += "Con: +" + row['Con Gains'] + " | "
    if (row['Mov Gains'] != '0'):
        if (int(row['Mov Gains']) > 0):
            gains += "Mov: +" + row['Mov Gains'] + " | "
        else:
            gains += "Mov: " + row['Mov Gains'] + " | "
    gains = gains[:-3]
    gains += "\n"
    if (row['Sword Gains'] != 'None'):
        if (row['Sword Gains'].isdigit()):
            gains += "Sword: +" + row['Sword Gains'] + " | "
        else:
            gains += "Sword: " + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
        if (row['Lance Gains'].isdigit()):
            gains += "Lance: +" + row['Lance Gains'] + " | "
        else:
            gains += "Lance: " + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
        if (row['Axe Gains'].isdigit()):
            gains += "Axe: +" + row['Axe Gains'] + " | "
        else:
            gains += "Axe: " + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
        if (row['Bow Gains'].isdigit()):
            gains += "Bow: +" + row['Bow Gains'] + " | "
        else:
            gains += "Bow: " + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
        if (row['Staff Gains'].isdigit()):
            gains += "Staff: +" + row['Staff Gains'] + " | "
        else:
            gains += "Staff: " + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
        if (row['Anima Gains'].isdigit()):
            gains += "Anima: +" + row['Anima Gains'] + " | "
        else:
            gains += "Anima: " + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
        if (row['Light Gains'].isdigit()):
            gains += "Light: +" + row['Light Gains'] + " | "
        else:
            gains += "Light: " + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
        if (row['Dark Gains'].isdigit()):
            gains += "Dark: +" + row['Dark Gains'] + " | "
        else:
            gains += "Dark: " + row['Dark Gains'] + " | "
    gains = gains[:-3]
    if (row['Promotes 2'] != 'No'): 
        gains += '\n' + row['Promotion Class 2'] + '\n'
        if (row['HP Gains 2'] != '0'):
            gains += "HP: +" + row['HP Gains 2'] + " | "
        if (row['Atk Gains 2'] != '0'):
            gains += "Atk: +" + row['Atk Gains 2'] + " | "
        if (row['Skl Gains 2'] != '0'):
            gains += "Skl: +" + row['Skl Gains 2'] + " | "
        if (row['Spd Gains 2'] != '0'):
            gains += "Spd: +" + row['Spd Gains 2'] + " | "
        if (row['Def Gains 2'] != '0'):
            gains += "Def: +" + row['Def Gains 2'] + " | "
        if (row['Res Gains 2'] != '0'):
            gains += "Res: +" + row['Res Gains 2'] + " | "
        if (row['Con Gains 2'] != '0'):
            gains += "Con: +" + row['Con Gains 2'] + " | "
        if (row['Mov Gains 2'] != '0'):
            if (int(row['Mov Gains 2']) > 0):
                gains += "Mov: +" + row['Mov Gains 2'] + " | "
            else:
                gains += "Mov: " + row['Mov Gains 2'] + " | "
        gains = gains[:-3]
        gains += "\n"
        if (row['Sword Gains 2'] != 'None'):
            if (row['Sword Gains 2'].isdigit()):
                gains += "Sword: +" + row['Sword Gains 2'] + " | "
            else:
                gains += "Sword: " + row['Sword Gains 2'] + " | "
        if (row['Lance Gains 2'] != 'None'):
            if (row['Lance Gains 2'].isdigit()):
                gains += "Lance: +" + row['Lance Gains 2'] + " | "
            else:
                gains += "Lance: " + row['Lance Gains 2'] + " | "
        if (row['Axe Gains 2'] != 'None'):
            if (row['Axe Gains 2'].isdigit()):
                gains += "Axe: +" + row['Axe Gains 2'] + " | "
            else:
                gains += "Axe: " + row['Axe Gains 2'] + " | "
        if (row['Bow Gains 2'] != 'None'):
            if (row['Bow Gains 2'].isdigit()):
                gains += "Bow: +" + row['Bow Gains 2'] + " | "
            else:
                gains += "Bow: " + row['Bow Gains 2'] + " | "
        if (row['Staff Gains 2'] != 'None'):
            if (row['Staff Gains 2'].isdigit()):
                gains += "Staff: +" + row['Staff Gains 2'] + " | "
            else:
                gains += "Staff: " + row['Staff Gains 2'] + " | "
        if (row['Anima Gains 2'] != 'None'):
            if (row['Anima Gains 2'].isdigit()):
                gains += "Anima: +" + row['Anima Gains 2'] + " | "
            else:
                gains += "Anima: " + row['Anima Gains 2'] + " | "
        if (row['Light Gains 2'] != 'None'):
            if (row['Light Gains 2'].isdigit()):
                gains += "Light: +" + row['Light Gains 2'] + " | "
            else:
                gains += "Light: " + row['Light Gains 2'] + " | "
        if (row['Dark Gains 2'] != 'None'):
            if (row['Dark Gains 2'].isdigit()):
                gains += "Dark: +" + row['Dark Gains 2'] + " | "
            else:
                gains += "Dark: " + row['Dark Gains 2'] + " | "
        gains = gains[:-3]
    if (row['Promotes 3'] != 'No'): 
        gains += '\n' + row['Promotion Class 3'] + '\n'
        if (row['HP Gains 3'] != '0'):
            gains += "HP: +" + row['HP Gains 3'] + " | "
        if (row['Atk Gains 3'] != '0'):
            gains += "Atk: +" + row['Atk Gains 3'] + " | "
        if (row['Skl Gains 3'] != '0'):
            gains += "Skl: +" + row['Skl Gains 3'] + " | "
        if (row['Spd Gains 3'] != '0'):
            gains += "Spd: +" + row['Spd Gains 3'] + " | "
        if (row['Def Gains 3'] != '0'):
            gains += "Def: +" + row['Def Gains 3'] + " | "
        if (row['Res Gains 3'] != '0'):
            gains += "Res: +" + row['Res Gains 3'] + " | "
        if (row['Con Gains 3'] != '0'):
            gains += "Con: +" + row['Con Gains 3'] + " | "
        if (row['Mov Gains 3'] != '0'):
            if (int(row['Mov Gains 3']) > 0):
                gains += "Mov: +" + row['Mov Gains 3'] + " | "
            else:
                gains += "Mov: " + row['Mov Gains 3'] + " | "
        gains = gains[:-3]
        gains += "\n"
        if (row['Sword Gains 3'] != 'None'):
            if (row['Sword Gains 3'].isdigit()):
                gains += "Sword: +" + row['Sword Gains 3'] + " | "
            else:
                gains += "Sword: " + row['Sword Gains 3'] + " | "
        if (row['Lance Gains 3'] != 'None'):
            if (row['Lance Gains 3'].isdigit()):
                gains += "Lance: +" + row['Lance Gains 3'] + " | "
            else:
                gains += "Lance: " + row['Lance Gains 3'] + " | "
        if (row['Axe Gains 3'] != 'None'):
            if (row['Axe Gains 3'].isdigit()):
                gains += "Axe: +" + row['Axe Gains 3'] + " | "
            else:
                gains += "Axe: " + row['Axe Gains 3'] + " | "
        if (row['Bow Gains 3'] != 'None'):
            if (row['Bow Gains 3'].isdigit()):
                gains += "Bow: +" + row['Bow Gains 3'] + " | "
            else:
                gains += "Bow: " + row['Bow Gains 3'] + " | "
        if (row['Staff Gains 3'] != 'None'):
            if (row['Staff Gains 3'].isdigit()):
                gains += "Staff: +" + row['Staff Gains 3'] + " | "
            else:
                gains += "Staff: " + row['Staff Gains 3'] + " | "
        if (row['Anima Gains 3'] != 'None'):
            if (row['Anima Gains 3'].isdigit()):
                gains += "Anima: +" + row['Anima Gains 3'] + " | "
            else:
                gains += "Anima: " + row['Anima Gains 3'] + " | "
        if (row['Light Gains 3'] != 'None'):
            if (row['Light Gains 3'].isdigit()):
                gains += "Light: +" + row['Light Gains 3'] + " | "
            else:
                gains += "Light: " + row['Light Gains 3'] + " | "
        if (row['Dark Gains 3'] != 'None'):
            if (row['Dark Gains 3'].isdigit()):
                gains += "Dark: +" + row['Dark Gains 3'] + " | "
            else:
                gains += "Dark: " + row['Dark Gains 3'] + " | "
        gains = gains[:-3]
    return gains

def setup(bot):
    bot.add_cog(Cota(bot))