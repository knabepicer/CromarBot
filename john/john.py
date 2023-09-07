import discord
import csv
import re
import random
from discord.ext import pages

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0xdeb41b)
    unitembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    #unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Atk " + row['Atk'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Atk " + row['Atk Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = john_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotes'] == "Yes"):
        gains = john_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)

    
    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        )
    ]
    
    return page_groups


#ee = cromar.create_subgroup("ee", "Get Embers Entwined data")

async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('john/john unit.csv', newline='', encoding="utf-8-sig") as csvfile:
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


def john_get_ranks(row):
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

def john_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != '0'):
        gains += "HP: " + row['HP Gains'] + " | "
    if (row['Atk Gains'] != '0'):
        gains += "Atk: " + row['Atk Gains'] + " | "
    if (row['Skl Gains'] != '0'):
        gains += "Skl: " + row['Skl Gains'] + " | "
    if (row['Spd Gains'] != '0'):
        gains += "Spd: " + row['Spd Gains'] + " | "
    if (row['Def Gains'] != '0'):
        gains += "Def: " + row['Def Gains'] + " | "
    if (row['Res Gains'] != '0'):
        gains += "Res: " + row['Res Gains'] + " | "
    if (row['Con Gains'] != '0'):
        gains += "Con: " + row['Con Gains'] + " | "
    if (row['Mov Gains'] != '0'):
        if (int(row['Mov Gains']) > 0):
            gains += "Mov: " + row['Mov Gains'] + " | "
        else:
            gains += "Mov: " + row['Mov Gains'] + " | "
    gains = gains[:-3]
    gains2 = "\n"
    if (row['Sword Gains'] != 'None'):
        if (row['Sword Gains'].isdigit()):
            gains2 += "<:RankSword:1083549037585768510>+" + row['Sword Gains'] + " | "
        else:
            gains2 += "<:RankSword:1083549037585768510>" + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
        if (row['Lance Gains'].isdigit()):
            gains2 += "<:RankLance:1083549035622846474>+" + row['Lance Gains'] + " | "
        else:
            gains2 += "<:RankLance:1083549035622846474>" + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
        if (row['Axe Gains'].isdigit()):
            gains2 += "<:RankAxe:1083549032292548659>+" + row['Axe Gains'] + " | "
        else:
            gains2 += "<:RankAxe:1083549032292548659>" + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
        if (row['Bow Gains'].isdigit()):
            gains2 += "<:RankBow:1083549033429205073>+" + row['Bow Gains'] + " | "
        else:
            gains2 += "<:RankBow:1083549033429205073>" + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
        if (row['Staff Gains'].isdigit()):
            gains2 += "<:RankStaff:1083549038936326155>+" + row['Staff Gains'] + " | "
        else:
            gains2 += "<:RankStaff:1083549038936326155>" + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
        if (row['Anima Gains'].isdigit()):
            gains2 += "<:RankAnima:1083549030598049884>+" + row['Anima Gains'] + " | "
        else:
            gains2 += "<:RankAnima:1083549030598049884>" + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
        if (row['Light Gains'].isdigit()):
            gains2 += "<:RankLight:1083549037019541614>+" + row['Light Gains'] + " | "
        else:
            gains2 += "<:RankLight:1083549037019541614>" + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
        if (row['Dark Gains'].isdigit()):
            gains2 += "<:RankDark:1083549034310012959>+" + row['Dark Gains'] + " | "
        else:
            gains2 += "<:RankDark:1083549034310012959>" + row['Dark Gains'] + " | "
    if len(gains2) > 0:
        gains2 = gains2[:-3]
    gains3 = ''
    gains4 = ''
    if (row['Promotes 2'] != 'No'): 
        gains3 += '\n' + row['Promotion Class 2'] + '\n'
        if (row['HP Gains 2'] != '0'):
            gains3 += "HP: " + row['HP Gains 2'] + " | "
        if (row['Atk Gains 2'] != '0'):
            gains3 += "Atk: " + row['Atk Gains 2'] + " | "
        if (row['Skl Gains 2'] != '0'):
            gains3 += "Skl: " + row['Skl Gains 2'] + " | "
        if (row['Spd Gains 2'] != '0'):
            gains3 += "Spd: " + row['Spd Gains 2'] + " | "
        if (row['Def Gains 2'] != '0'):
            gains3 += "Def: " + row['Def Gains 2'] + " | "
        if (row['Res Gains 2'] != '0'):
            gains3 += "Res: " + row['Res Gains 2'] + " | "
        if (row['Con Gains 2'] != '0'):
            if (int(row['Con Gains 2']) > 0):
                gains3 += "Con: " + row['Con Gains 2'] + " | "
            else:
                gains3 += "Con: " + row['Con Gains 2'] + " | "
        if (row['Mov Gains 2'] != '0'):
            if (int(row['Mov Gains 2']) > 0):
                gains3 += "Mov: " + row['Mov Gains 2'] + " | "
            else:
                gains3 += "Mov: " + row['Mov Gains 2'] + " | "
        if len(gains3) > 0:
            gains3 = gains3[:-3]
        gains4 += "\n"
        if (row['Sword Gains 2'] != 'None'):
            if (row['Sword Gains 2'].isdigit()):
                gains4 += "<:RankSword:1083549037585768510>+" + row['Sword Gains 2'] + " | "
            else:
                gains4 += "<:RankSword:1083549037585768510>" + row['Sword Gains 2'] + " | "
        if (row['Lance Gains 2'] != 'None'):
            if (row['Lance Gains 2'].isdigit()):
                gains4 += "<:RankLance:1083549035622846474>+" + row['Lance Gains 2'] + " | "
            else:
                gains4 += "<:RankLance:1083549035622846474>" + row['Lance Gains 2'] + " | "
        if (row['Axe Gains 2'] != 'None'):
            if (row['Axe Gains 2'].isdigit()):
                gains4 += "<:RankAxe:1083549032292548659>+" + row['Axe Gains 2'] + " | "
            else:
                gains4 += "<:RankAxe:1083549032292548659>" + row['Axe Gains 2'] + " | "
        if (row['Bow Gains 2'] != 'None'):
            if (row['Bow Gains 2'].isdigit()):
                gains4 += "<:RankBow:1083549033429205073>+" + row['Bow Gains 2'] + " | "
            else:
                gains4 += "<:RankBow:1083549033429205073>" + row['Bow Gains 2'] + " | "
        if (row['Staff Gains 2'] != 'None'):
            if (row['Staff Gains 2'].isdigit()):
                gains4 += "<:RankStaff:1083549038936326155>+" + row['Staff Gains 2'] + " | "
            else:
                gains4 += "<:RankStaff:1083549038936326155>" + row['Staff Gains 2'] + " | "
        if (row['Anima Gains 2'] != 'None'):
            if (row['Anima Gains 2'].isdigit()):
                gains4 += "<:RankAnima:1083549030598049884>+" + row['Anima Gains 2'] + " | "
            else:
                gains4 += "<:RankAnima:1083549030598049884>" + row['Anima Gains 2'] + " | "
        if (row['Light Gains 2'] != 'None'):
            if (row['Light Gains 2'].isdigit()):
                gains4 += "<:RankLight:1083549037019541614>+" + row['Light Gains 2'] + " | "
            else:
                gains4 += "<:RankLight:1083549037019541614>" + row['Light Gains 2'] + " | "
        if (row['Dark Gains 2'] != 'None'):
            if (row['Dark Gains 2'].isdigit()):
                gains4 += "<:RankDark:1083549034310012959>+" + row['Dark Gains 2'] + " | "
            else:
                gains4 += "<:RankDark:1083549034310012959>" + row['Dark Gains 2'] + " | "
        if len(gains4) > 0:
            gains4 = gains4[:-3]
    return gains + gains2 + gains3 + gains4



def get_unit_names(ctx):
    names = ["John","Joe","Ekram","Saif","Andrew","Joseph","Salman","Jojo","Carol","Carl","Layan","Raina"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
