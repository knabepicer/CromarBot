import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x0d59d4)
    supportembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x0d59d4)
    
    unitembed.set_thumbnail(url=row['Portrait'])
    supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    
    unitembed.add_field(name='Army: ', value=row['Army'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] +  " | " + "Mag " + row['Mag'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Mov']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | " + "Mag " + row['Mag Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = fourkings_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotes'] == "Yes"):
        gains = fourkings_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    caps ="Str " + row['Str Cap'] +  " | " + "Mag " + row['Mag Cap'] + " | Skl " + row['Skl Cap'] + " | " + "Spd " + row['Spd Cap'] + " | " + "Def " + row['Def Cap'] + " | " + "Res " + row['Res Cap']
    unitembed.add_field(name="Caps", value=caps, inline=False)
    if (row["Name"] == "Sarah"):
        unitembed.set_footer(text="Sarah possesses the skill Outrider, which grants her -1 damage taken, and +3% crit, per space moved.")
    with open('fourkings/four kings support.csv', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        supportstring = ""
        for supportrow in reader:
            if (row['Name'] == 'Walter'):
                supportstring = "End of Chapter 3: Walter/Ava C\nEnd of Intermission: Walter/Ava B\nEnd of Chapter 19: Walter/Ava A\nEnd of Reunion: Walter/Lionel B\nEnd of Chapter 22: Walter/Terril B"
            elif (row['Name'] == 'Ava'):
                supportstring = "End of Chapter 3: Walter/Ava C\nEnd of Intermission: Walter/Ava B\nEnd of Chapter 19: Walter/Ava A\nEnd of Chapter 24: Ava/Marvin B"  
            elif (row['Name'] == 'Lionel'):
                supportstring = "End of Chapter 3: Lionel/Zach C\nEnd of Reunion: Walter/Lionel B, Lionel/Zach B\nEnd of Chapter 22: Lionel/Terril B"
            elif (row['Name'] == 'Zach'):
                supportstring = "End of Chapter 3: Lionel/Zach C\nEnd of Reunion: Lionel/Zach B"
            elif (row['Name'] == "Terril"):
                supportstring = "End of Chapter 22: Walter/Terril B, Lionel/Terril B"
            elif (row['Name'] == "Marvin"):
                supportstring = "End of Chapter 24: Ava/Marvin B"
            elif(row['Name'] == supportrow['Name']):
                if(supportrow['Partner 1'] != ''):
                    supportstring += supportrow['Partner 1'] + " : Base: " + supportrow['Base 1'] + " | Growth: +" + supportrow['Growth 1'] + "\n"
                if(supportrow['Partner 2'] != ''):
                    supportstring += supportrow['Partner 2'] + " : Base: " + supportrow['Base 2'] + " | Growth: +" + supportrow['Growth 2'] + "\n"
                if(supportrow['Partner 3'] != ''):
                    supportstring += supportrow['Partner 3'] + " : Base: " + supportrow['Base 3'] + " | Growth: +" + supportrow['Growth 3'] + "\n"
                if(supportrow['Partner 4'] != ''):
                    supportstring += supportrow['Partner 4'] + " : Base: " + supportrow['Base 4'] + " | Growth: +" + supportrow['Growth 4'] + "\n"
                if(supportrow['Partner 5'] != ''):
                    supportstring += supportrow['Partner 5'] + " : Base: " + supportrow['Base 5'] + " | Growth: +" + supportrow['Growth 5'] + "\n"
                #if(supportrow['Partner 6'] != ''):
                #    supportstring += supportrow['Partner 6'] + " : Base: " + supportrow['Base 6'] + " | Growth: +" + supportrow['Growth 6'] + "\n"
                #if(supportrow['Partner 7'] != ''):
                #    supportstring += supportrow['Partner 7'] + " : Base: " + supportrow['Base 7'] + " | Growth: +" + supportrow['Growth 7'] + "\n" 
        supportembed.add_field(name="", value=supportstring, inline=False)
        #supportembed.add_field(name="test", value="test2", inline=False)
        supportembed.set_footer(text="See affinity bonuses here: https://feuniverse.us/t/fe8-complete-fire-emblem-the-four-kings-4-11-24-update-now-with-weapon-reversal/7030")
    


    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        ),
        pages.PageGroup(
        pages=[supportembed],
        label="Supports",
        description="Support data for the unit",
        use_default_buttons=False,
        ), 
        
    ]

    if (row['PRF Name'] != ""):
        prfembed=discord.Embed(title=row['Name'], color=0x0d59d4)
        #prfembed.set_thumbnail(url=row['PRF Icon'])
        if(row['PRF Type'] != 'Staff'):
            stats = "Type: " + row['PRF Type'] + " | Mt: " + row['PRF Mt'] + " | Hit: " + row['PRF Hit'] + " | Crit: " + row['PRF Crit'] + " | Wt: " + row['PRF Wt'] + " | Range: " + row['PRF Rng']
            stats += " | Uses: " + row['PRF Dur']
            if (row['PRF Desc'] != ""):
                stats += '\n'
                stats += row['PRF Desc']
        else:
            stats  = "Type: " + row['PRF Type'] + " | Range: " + row['PRF Rng'] + " | Uses: " + row['PRF Dur']
            stats += '\n'
            stats += row['PRF Desc']
        prfembed.add_field(name=row['PRF Name'], value=stats, inline=False)
        if (row['PRF Name 2'] != ""):
            if(row['PRF Type 2'] != 'Staff'):
                stats2 = "Type: " + row['PRF Type 2'] + " | Mt: " + row['PRF Mt 2'] + " | Hit: " + row['PRF Hit 2'] + " | Crit: " + row['PRF Crit 2'] + " | Wt: " + row['PRF Wt 2'] + " | Range: " + row['PRF Rng 2']
                stats2 += " | Uses: " + row['PRF Dur 2']
                if (row['PRF Desc 2'] != ""):
                    stats2 += '\n'
                    stats2 += row['PRF Desc 2']
            else:
                stats2  = "Type: " + row['PRF Type 2'] + " | Range: " + row['PRF Rng 2'] + " | Uses: " + row['PRF Dur 2']
                stats2 += '\n'
                stats2 += row['PRF Desc 2']
            prfembed.add_field(name=row['PRF Name 2'], value=stats2, inline=False)


        page_groups.append(pages.PageGroup(
        pages=[prfembed], 
        label="Prf Weapon Data",
        description="Information about this unit's prfs",
        use_default_buttons=False,
        default=False,
        ))
    return page_groups


async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('fourkings/four kings unit.csv', newline='') as csvfile:
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

def fourkings_get_ranks(row):
    ranks = ""
    if (row['Sword'] != 'NoRank'):
        ranks += "<:RankSword:1083549037585768510>Sword: " + row['Sword'] + " | "
    if (row['Lance'] != 'NoRank'):
        ranks += "<:RankLance:1083549035622846474>Lance: " + row['Lance'] + " | "
    if (row['Axe'] != 'NoRank'):
        ranks += "<:RankAxe:1083549032292548659>Axe: " + row['Axe'] + " | "
    if (row['Bow'] != 'NoRank'):
        ranks += "<:RankBow:1083549033429205073>Bow: " + row['Bow'] + " | "
    if (row['Staff'] != 'NoRank'):
        ranks += "<:RankStaff:1083549038936326155>Staff: " + row['Staff'] + " | "
    if (row['Anima'] != 'NoRank'):
        ranks += "<:RankAnima:1083549030598049884>Anima: " + row['Anima'] + " | "
    if (row['Light'] != 'NoRank'):
        ranks += "<:RankLight:1083549037019541614>Light: " + row['Light'] + " | "
    if (row['Dark'] != 'NoRank'):
        ranks += "<:RankDark:1083549034310012959>Dark: " + row['Dark'] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "None"
    return ranks

def fourkings_get_gains(row):
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
    gains = gains + gains2
    if (row['Promotes 2'] == 'Yes'):
        gains3 = ""
        gains3 += row['Promotion Class 2'] + '\n'
        if (row['HP Gains 2'] != '0'):
            gains3 += "HP: +" + row['HP Gains 2'] + " | "
        if (row['Str Gains 2'] != '0'):
            gains3 += "Str: +" + row['Str Gains 2'] + " | "
        if (row['Mag Gains 2'] != '0'):
            gains3 += "Mag: +" + row['Mag Gains 2'] + " | "
        if (row['Skl Gains 2'] != '0'):
            gains3 += "Skl: +" + row['Skl Gains 2'] + " | "
        if (row['Spd Gains 2'] != '0'):
            gains3 += "Spd: +" + row['Spd Gains 2'] + " | "
        if (row['Def Gains 2'] != '0'):
            gains3 += "Def: +" + row['Def Gains 2'] + " | "
        if (row['Res Gains 2'] != '0'):
            gains3 += "Res: +" + row['Res Gains 2'] + " | "
        if (row['Con Gains 2'] != '0'):
            gains3 += "Con: +" + row['Con Gains 2'] + " | "
        if (row['Mov Gains 2'] != '0'):
            if (int(row['Mov Gains 2']) > 0):
                gains3 += "Mov: +" + row['Mov Gains 2'] + " | "
            else:
                gains3 += "Mov: " + row['Mov Gains 2'] + " | "
        gains3 = gains3[:-3]
        gains3 += "\n"
        gains4 = ""
        if (row['Sword Gains 2'] != 'None'):
                gains4 += "<:RankSword:1083549037585768510>" + row['Sword Gains 2'] + " | "
        if (row['Lance Gains 2'] != 'None'):
                gains4 += "<:RankLance:1083549035622846474>" + row['Lance Gains 2'] + " | "
        if (row['Axe Gains 2'] != 'None'):
                gains4 += "<:RankAxe:1083549032292548659>" + row['Axe Gains 2'] + " | "
        if (row['Bow Gains 2'] != 'None'):
                gains4 += "<:RankBow:1083549033429205073>" + row['Bow Gains 2'] + " | "
        if (row['Staff Gains 2'] != 'None'):
                gains4 += "<:RankStaff:1083549038936326155>" + row['Staff Gains 2'] + " | "
        if (row['Anima Gains 2'] != 'None'):
                gains4 += "<:RankAnima:1083549030598049884>" + row['Anima Gains 2'] + " | "
        if (row['Light Gains 2'] != 'None'):
                gains4 += "<:RankLight:1083549037019541614>" + row['Light Gains 2'] + " | "
        if (row['Dark Gains 2'] != 'None'):
                gains4 += "<:RankDark:1083549034310012959>" + row['Dark Gains 2'] + " | "
        if (len(gains2) > 0):
            gains4 = gains4[:-3]
        gains = gains + "\n" + gains3 + gains4
         
    return gains

def get_unit_names(ctx):
    names = ["Walter","Lionel","Zachary","Bradley","Shaun","Chase","Lydia","Shelby","Yufin","Ava","Max","Sally","Marcie","Dorian","Zoe","Vin","Cielo","Victor","Ron","Locritus","Colt","Hoff","Cindy","Regis","Wilson","Terry","Harriet","Patty","Candace","Jack","Jeremy","Sarah","Alicia","Elias","Nicole","Gideon","Luceil","Emily","Terril","Marvin"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]