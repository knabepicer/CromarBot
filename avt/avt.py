import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'], color=0xd85d5d)
    #supportembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x34c290)
    unitembed.set_thumbnail(url=row['Portrait'])
    #supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] + " | " + "Mag " + row['Mag'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Mov']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | " + "Mag " + row['Mag Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = avt_get_ranks(row)
    unitembed.add_field(name="Skills", value=row['Skills'], inline=False)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotion Class'] != ""):
        gains = avt_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    
    # with open('trtr/trtr supports.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for supportrow in reader:
    #         if(row['Name'] == supportrow['Name']):
    #             supportstring = ""
    #             if(supportrow['Partner 1'] != 'None'):
    #                 supportstring += supportrow['Partner 1'] + " : Base: " + supportrow['Starting Value 1'] + " | Growth: +" + supportrow['Growth 1'] + "\n"
    #             supportembed.add_field(name="", value=supportstring, inline=False)


    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        ),
        # pages.PageGroup(
        # pages=[supportembed],
        # label="Supports",
        # description="Support data for the unit",
        # use_default_buttons=False,
        # )
    ]

    return page_groups
    


async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('avt/avt unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                paginator = pages.Paginator(pages=get_unit_pages(row), show_menu=True, show_disabled=False, show_indicator=False, menu_placeholder="Select page to view", timeout =120, disable_on_timeout = True)
                await paginator.respond(ctx.interaction)
                was_found = True
                break
        if (not was_found):
            await ctx.response.send_message("That unit does not exist.")

""" async def skill(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('avt/avt skill.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                unitembed=discord.Embed(title=row['Name'], color=0x34c290)
                unitembed.add_field(name='Description: ', value=row['Description'], inline=False)
                was_found = True
                await ctx.response.send_message(embed=unitembed)
                break
        if (not was_found):
                await ctx.response.send_message("That skill does not exist.") """


def avt_get_ranks(row):
    ranks = ""
    if (row['Sword'] != 'None'):
        ranks += "<:RankSword:1083549037585768510>Sword: " + row['Sword'] + " | "
    if (row['Lance'] != 'None'):
        ranks += "<:RankLance:1083549035622846474>Lance: " + row['Lance'] + " | "
    if (row['Axe'] != 'None'):
        ranks += "<:RankAxe:1083549032292548659>Axe: " + row['Axe'] + " | "
    if (row['Bow'] != 'None'):
        ranks += "<:RankBow:1083549033429205073>Bow: " + row['Bow'] + " | "
    if (row['Staff'] != 'None'):
        ranks += "<:RankStaff:1083549038936326155>Staff: " + row['Staff'] + " | "
    if (row['Anima'] != 'None'):
        ranks += "<:RankAnima:1083549030598049884>Anima: " + row['Anima'] + " | "
    if (row['Light'] != 'None'):
        ranks += "<:RankLight:1083549037019541614>Light: " + row['Light'] + " | "
    if (row['Dark'] != 'None'):
        ranks += "<:RankDark:1083549034310012959>Dark: " + row['Dark'] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "None"
    return ranks

def avt_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != '0'):
        gains += "HP: +" + row['HP Gains'] + " | "
    if (row['Str Gains'] != '0'):
        gains += "Str: +" + row['Str Gains'] + " | "
    if (row['Mag Gains'] != '0'):
        gains += "Mag: +" + row['Str Gains'] + " | "
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
    gains2 = ""
    if (row['Sword Gains'] != 'None'):
            gains2 += "<:RankSword:1083549037585768510>" + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
            gains2 += "<:RankLance:1083549035622846474>" + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
            gains2 += "<:RankAxe:1083549032292548659>" + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
            gains2 += "<:RankBow:1083549033429205073>" + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
            gains2 += "<:RankStaff:1083549038936326155>" + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
            gains2 += "<:RankAnima:1083549030598049884>" + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
            gains2 += "<:RankLight:1083549037019541614>" + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
            gains2 += "<:RankDark:1083549034310012959>" + row['Dark Gains'] + " | "
    if (len(gains2) > 0):
        gains2 = gains2[:-3]
    return gains + gains2

def get_unit_names(ctx):
    names = ["Alva","Alyssa","Anatolij","Angelo","Carmela","Coventry","Cynthia","Escarra","Ezekiel","Firenze","Ginepro","Helena","Iblis","Irene","Jerez","Lafayette","Laurencio","Liquirizia","Magritte","Marzano","Ms. Parsley","Samir","Sanzang","Schmidt","Terry","Yehoshua"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

""" def get_skill_names(ctx):
    names = ["Charisma","Pass","Nihil","Gentilhomme","Miracle","Light Weight","Swap","Strong Riposte","Wrath","Spur Resistance","Bond","Quick Burn","Intimidate","Savior","Reposition","Spur Strength","Pivot","Knight Aspirant","Slow Burn","Acrobat","Vantage","Spur Magic","Darting Blow","Thunderstorm","Puissance","Demoiselle","Charm","Spur Speed","Spur Defense","Summon","Paragon","Hex","Pursuit","Heavy Strikes","Inspiration","Lily's Poise","Chivalry","Pragmatic","Anathema","Death Blow","Boon","Armored Blow","Perfectionist","Fiery Blood","Even Rhythm","Frenzy","Triangle Adept","Tantivy","Nullify","Duelist's Blow","Odd Rhythm","Vanity","Infiltrator","Opportunist","Relief","Desperation","Staff Savant","Shove","Quick Draw","Natural Cover","Cunning","Steal","Crit Boost","Certain Blow","Forager","Discipline+","Live to Serve","Locktouch","Steal+","Breath of Life","Wind Disciple","Voice of Peace","Camaraderie"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())] """
