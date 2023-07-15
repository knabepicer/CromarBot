import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0xd9d021)
    #supportembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0xd9d021)
    sidesembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0xd9d021)
    unitembed.set_thumbnail(url=row['Portrait'])
    #supportembed.set_thumbnail(url=row['Portrait'])
    sidesembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    unitembed.add_field(name="Leadership: ", value=row['Leadership'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] + " | Mag " + row['Mag'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Mov']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | Mag " + row['Mag Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = burger_get_ranks(row)
    unitembed.add_field(name="Skills", value=row['Skills'], inline=False)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotion Class'] != ""):
        gains = burger_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    
    # with open('trtr/trtr supports.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for supportrow in reader:
    #         if(row['Name'] == supportrow['\ufeffName']):
    #             supportstring = ""
    #             if(supportrow['Partner 1'] != 'None'):
    #                 supportstring += supportrow['Partner 1'] + " : Base: " + supportrow['Starting Value 1'] + " | Growth: +" + supportrow['Growth 1'] + "\n"
    #             supportembed.add_field(name="", value=supportstring, inline=False)
    with open('burger/burger_sides.csv', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for sidesrow in reader:
            if(row['Name'] == sidesrow['Name']):
                if (sidesrow['Special'] == 'Yes'):
                    sidesembed.add_field(name="", value="Special Class", inline=True)
                onea = burger_get_sides_info(sidesrow, " 1A")
                sidesembed.add_field(name="First B-Side", value=onea, inline=True)
                if (sidesrow['Recursive'] != 'Yes'):
                    oneb = burger_get_sides_info(sidesrow, " 1B")
                    sidesembed.add_field(name="Second B-Side", value=oneb, inline=True)
                    if (sidesrow['Promotion Class'] != ''):
                        sidesembed.add_field(name='Promoted Class', value=sidesrow['Promotion Class'], inline=True)
                        twoa = burger_get_sides_info(sidesrow, " 2A")
                        sidesembed.add_field(name="First Promoted B-Side", value=twoa, inline=True)
                        twob = burger_get_sides_info(sidesrow, " 2B")
                        sidesembed.add_field(name="Second Promoted B-Side", value=twob, inline=True)
                if (sidesrow['Note'] != ""):
                    sidesembed.set_footer(text=sidesrow['Note'])
                     


    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        ),
         pages.PageGroup(
         pages=[sidesembed],
         label="B-Sides",
         description="Data for up to the first two B-Sides for unit",
         use_default_buttons=False,
         )
    ]

    return page_groups
    


async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('burger/burger_unit.csv', newline='', encoding="utf-8-sig") as csvfile:
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

async def skill(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('burger/burger_skill.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                unitembed=discord.Embed(title=row['Name'], color=0xd9d021)
                unitembed.add_field(name='Description: ', value=row['Description'], inline=False)
                was_found = True
                await ctx.response.send_message(embed=unitembed)
                break
        if (not was_found):
                await ctx.response.send_message("That skill does not exist.")


def burger_get_ranks(row):
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

def burger_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != '0'):
        gains += "HP: +" + row['HP Gains'] + " | "
    if (row['Str Gains'] != '0'):
        gains += "Str: +" + row['Str Gains'] + " | "
    if (row['Mag Gains'] != '0'):
        gains += "Mag: +" + row['Mag Gains'] + " | "
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

def burger_get_sides_info(row, suffix):
    total = ""
    gains = ""
    total += row['B-Sides Class' + suffix] + "\n"
    if (row['HP Gains' + suffix] != '0'):
        gains += "HP: +" + row['HP Gains'+ suffix] + " | "
    if (row['Str Gains'+ suffix] != '0'):
        gains += "Str: +" + row['Str Gains'+ suffix] + " | "
    if (row['Mag Gains'+ suffix] != '0'):
        gains += "Mag: +" + row['Mag Gains'+ suffix] + " | "
    if (row['Skl Gains'+ suffix] != '0'):
        gains += "Skl: +" + row['Skl Gains'+ suffix] + " | "
    if (row['Spd Gains'+ suffix] != '0'):
        gains += "Spd: +" + row['Spd Gains'+ suffix] + " | "
    if (row['Def Gains'+ suffix] != '0'):
        gains += "Def: +" + row['Def Gains'+ suffix] + " | "
    if (row['Res Gains'+ suffix] != '0'):
        gains += "Res: +" + row['Res Gains'+ suffix] + " | "
    if (row['Con Gains'+ suffix] != '0'):
        if (int(row['Con Gains'+ suffix]) > 0):
            gains += "Con: +" + row['Con Gains'+ suffix] + " | "
        else:
            gains += "Con: " + row['Con Gains'+ suffix] + " | "
    if (row['Mov Gains'+ suffix] != '0'):
        if (int(row['Mov Gains'+ suffix]) > 0):
            gains += "Mov: +" + row['Mov Gains'+ suffix] + " | "
        else:
            gains += "Mov: " + row['Mov Gains'+ suffix] + " | "
    if (len(gains) > 0):
        gains = gains[:-3]
        gains += "\n"
    ranks = ""
    if (row['New Sword'+ suffix] != 'None'):
        ranks += "<:RankSword:1083549037585768510>Sword: " + row['New Sword'+ suffix] + " | "
    if (row['New Lance'+ suffix] != 'None'):
        ranks += "<:RankLance:1083549035622846474>Lance: " + row['New Lance'+ suffix] + " | "
    if (row['New Axe'+ suffix] != 'None'):
        ranks += "<:RankAxe:1083549032292548659>Axe: " + row['New Axe'+ suffix] + " | "
    if (row['New Bow'+ suffix] != 'None'):
        ranks += "<:RankBow:1083549033429205073>Bow: " + row['New Bow'+ suffix] + " | "
    if (row['New Staff'+ suffix] != 'None'):
        ranks += "<:RankStaff:1083549038936326155>Staff: " + row['New Staff'+ suffix] + " | "
    if (row['New Anima'+ suffix] != 'None'):
        ranks += "<:RankAnima:1083549030598049884>Anima: " + row['New Anima'+ suffix] + " | "
    if (row['New Light'+ suffix] != 'None'):
        ranks += "<:RankLight:1083549037019541614>Light: " + row['New Light'+ suffix] + " | "
    if (row['New Dark'+ suffix] != 'None'):
        ranks += "<:RankDark:1083549034310012959>Dark: " + row['New Dark'+ suffix] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "Ricardo"
    total += gains + ranks
    return total


def get_unit_names(ctx):
    names = ["BK","Sephiran","Fiona","Hugh","Chungis","Dalvin","Sharlow","Matthis","Soldier","Rebecca","Priscilla","Sail","Perne","Trude","Lynhardt","Salem","Brown","Kaga","Rad Quetz","Tomas","Generic Ilian","ST4F-BOT","Bigle","Deke","Bors","Marty","Azel","Bernie","The King","Papaya","Not Kelik","Honse","Samto","Demijagen","Wario","Ricardo","Dorshua","Subject 35","Joshua","Butter Dog","Riddel","Tailtiu","Kempf","Adachy"]
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

def get_skill_names(ctx):
    names = []
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
