import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'], color=0x252926)
    #supportembed=discord.Embed(title=row['Name'], color=0x252926)
    if (row['Name'] == 'Lilim' and random.randint(1, 10) == 1):
        unitembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1043928901610643456/1103132562534178877/lilim_hairflip.gif")
    elif (row['Name'] == 'Haban' and random.randint(1, 10) == 1):
         unitembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1043928901610643456/1103132628242149486/haban_alt_1.png")
    else:
        unitembed.set_thumbnail(url=row['Portrait'])
    #supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] +  " | " + "Mag " + row['Mag'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | " + "Mag " + row['Mag Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = sp_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotion Class'] != ""):
        gains = sp_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    if (row['Bonus 2'] != "None"):
        unitembed.set_footer(text=row['Bonus 2'])
    # with open('dow/dow supports.csv', newline='') as csvfile:
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

    if (row['Name'] == 'Evans' or row['Name'] == 'Madari'):
        with open('sp/sp unit.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for newrow in reader:
                if((row['Name'] + " Late") == newrow['Name']):
                    newembed=discord.Embed(title=newrow['Name'], color=0x252926)

                    newembed.set_thumbnail(url=newrow['Portrait'])

                    newembed.add_field(name="Lv " + newrow['Lv'] + " ", value=newrow['Class'], inline=True)
                    newembed.add_field(name="Affinity: ", value=newrow['Affinity'], inline=True)
                    bases = "HP " + newrow['HP'] + " | " + "Str " + newrow['Str'] +  " | " + "Mag " + newrow['Mag'] + " | Skl " + newrow['Skl'] + " | " + "Spd " + newrow['Spd'] + " | " + "Lck " + newrow['Luck'] + " | " + "Def " + newrow['Def'] + " | " + "Res " + newrow['Res'] + " | " + "Con " + newrow['Con'] + " | " + "Mov " + newrow['Move']
                    newembed.add_field(name="Bases", value=bases, inline=False)
                    growths = "HP " + newrow['HP Growth'] + "% | " + "Str " + newrow['Str Growth'] + "% | " + "Mag " + newrow['Mag Growth'] + "% | Skl " + newrow['Skl Growth'] + "% | " + "Spd " + newrow['Spd Growth'] + "% | " + "Lck " + newrow['Luck Growth'] + "% | " + "Def " + newrow['Def Growth'] + "% | " + "Res " + newrow['Res Growth'] + "%"
                    newembed.add_field(name="Growths", value=growths, inline=False)
                    ranks = sp_get_ranks(newrow)
                    newembed.add_field(name="Ranks", value=ranks, inline=False)
                    page_groups.append(pages.PageGroup(
        pages=[newembed], 
        label="Alternate Unit Data",
        description="Unit data for this unit's late recruitment.",
        use_default_buttons=False,
        default=False,))
                

    return page_groups
    


async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('sp/sp unit.csv', newline='') as csvfile:
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


def sp_get_ranks(row):
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

def sp_get_gains(row):
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
    if (row['Bonus'] != "None"):
        gains2 += "\n" + row['Bonus']
    return gains + gains2

def get_unit_names(ctx):
    names = ["Prosel","Haban","Lou","Annie","Hute","Marilyn","Eileen","Darrel","Cyrus","Majen","Grant","Silph","Eddie","Colton","Vesper","Alta","Dour","Clint","Demi","Wyler","Nello","Bast","Melanie","Lilim","Eliza","Peirhok","Cadence","Vicks","Barbara","Orville","Onick","Ruben","Madari","Evans","Boddason","Lyra","Nidas","Krunk","Rita","Ray","Kassandra","Carrie","Aster"]
    return [name for name in names if name.lower().startswith(ctx.value.lower())]