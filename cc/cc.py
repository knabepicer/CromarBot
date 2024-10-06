import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'], color=0x59cad9)
   # supportembed=discord.Embed(title=row['Name'], color=0x0d59d4)
    
    unitembed.set_thumbnail(url=row['Portrait'])
   # supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    unitembed.add_field(name="Leadership: ", value=row['Leadership'], inline=True)
    
    bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] +  " | " + "Mag " + row['Mag'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Mov']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | " + "Mag " + row['Mag Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    if (row['Skills'] != ""):
        unitembed.add_field(name="Skills", value=row['Skills'], inline=False)
    if (row['Prf'] != ""):
        unitembed.add_field(name="Prfs", value=row['Prf'], inline=False)
    ranks = cc_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotion Class'] != ""):
        gains = cc_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)

    


    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        ), 
    ]

    if (row['Prf'] != "" or row['Skills'] != ""):
        prfembed=discord.Embed(title=row['Name'], color=0x59cad9)
        #prfembed.set_thumbnail(url=row['PRF Icon'])
        if (row['Prf Name'] != ""):
            if(row['Prf Weapon Type'] != 'Staff'):
                stats = "Type: " + row['Prf Weapon Type'] + " | Mt: " + row['Prf Mt'] + " | Hit: " + row['Prf Hit'] + " | Crit: " + row['Prf Crit'] + " | Wt: " + row['Prf Wt'] + " | Range: " + row['Prf Range']
                stats += " | Uses: " + row['Prf Uses']
                if (row['Prf Description'] != ""):
                    stats += '\n'
                    stats += row['Prf Description']
            else:
                stats  = "Type: " + row['Prf Weapon Type'] + " | Range: " + row['Prf Range'] + " | Uses: " + row['Prf Uses']
                stats += '\n'
                stats += row['Prf Description']
            prfembed.add_field(name=row['Prf Name'], value=stats, inline=False)
        if (row['Prf Name 2'] != ""):
            if(row['Prf Weapon Type 2'] != 'Staff'):
                stats = "Type: " + row['Prf Weapon Type 2'] + " | Mt: " + row['Prf Mt 2'] + " | Hit: " + row['Prf Hit 2'] + " | Crit: " + row['Prf Crit 2'] + " | Wt: " + row['Prf Wt 2'] + " | Range: " + row['Prf Range 2']
                stats += " | Uses: " + row['Prf Uses 2']
                if (row['Prf Description 2'] != ""):
                    stats += '\n'
                    stats += row['Prf Description 2']
            else:
                stats  = "Type: " + row['Prf Weapon Type 2'] + " | Range: " + row['Prf Range 2'] + " | Uses: " + row['Prf Uses 2']
                stats += '\n'
                stats += row['Prf Description 2']
            prfembed.add_field(name=row['Prf Name 2'], value=stats, inline=False)
        if (row['Prf Name 3'] != ""):
            if(row['Prf Weapon Type 3'] != 'Staff'):
                stats = "Type: " + row['Prf Weapon Type 3'] + " | Mt: " + row['Prf Mt 3'] + " | Hit: " + row['Prf Hit 3'] + " | Crit: " + row['Prf Crit 3'] + " | Wt: " + row['Prf Wt 3'] + " | Range: " + row['Prf Range 3']
                stats += " | Uses: " + row['Prf Uses 3']
                if (row['Prf Description 3'] != ""):
                    stats += '\n'
                    stats += row['Prf Description 3']
            else:
                stats  = "Type: " + row['Prf Weapon Type 3'] + " | Range: " + row['Prf Range 3'] + " | Uses: " + row['Prf Uses 3']
                stats += '\n'
                stats += row['Prf Description 3']
            prfembed.add_field(name=row['Prf Name 3'], value=stats, inline=False)
        if (row['Skill Name 1'] != ''):
            prfembed.add_field(name=row['Skill Name 1'], value=row['Skill Desc 1'], inline=False)
        if (row['Skill Name 2'] != ''):
            prfembed.add_field(name=row['Skill Name 2'], value=row['Skill Desc 2'], inline=False)
        if (row['Skill Name 3'] != ''):
            prfembed.add_field(name=row['Skill Name 3'], value=row['Skill Desc 3'], inline=False)
        if (row['Skill Name 4'] != ''):
            prfembed.add_field(name=row['Skill Name 4'], value=row['Skill Desc 4'], inline=False)

        page_groups.append(pages.PageGroup(
        pages=[prfembed], 
        label="Prf/Skill Data",
        description="Information about this unit's prfs and skills",
        use_default_buttons=False,
        default=False,
        ))
    return page_groups


async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('cc/cc units.csv', newline='') as csvfile:
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

async def item(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)            
    with open('cc/cc items.csv', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            #print(stripped_row)
            if(stripped_row.lower() == stripped_name.lower()):
                unitembed=discord.Embed(title=row['Name'], color=0x59cad9)
                #unitembed.set_thumbnail(url=row['Icon'])
                if(row['Type'] == 'Weapon'):
                    stats = "Rank: " + row['Weapon Level'] + " | Mt: " + row['Mt'] + " | Hit: " + row['Hit'] + " | Crit: " + row['Crit'] + " | Wt: " + row['Wt'] + " | Range: " + row['Range'] #+ " | WEXP: " + row['WEXP']
                    if (row['Uses'] == '255'):
                        stats += " | Unbreakable"
                    else:
                        stats += " | Uses: " + row['Uses']
                    if (row['Description'] != ""):
                        stats += '\n'
                        stats += row['Description']
                    unitembed.add_field(name=row['Weapon Type'], value=stats, inline=False)
                elif(row['Type'] == 'Staff'):
                    stats  = "Rank: " + row['Weapon Level'] + " | Wt: " + row['Wt'] + " | Range: " + row['Range'] + " | WEXP: " + row['WEXP'] + " | Uses: " + row['Uses']
                    stats += '\n'
                    stats += row['Description']
                    unitembed.add_field(name='Staff', value=stats, inline=False)
                elif(row['Type'] == 'Item'):
                    stats = ""
                    if (row['Uses'] == '255'):
                        stats += "Unbreakable"
                    else:
                        stats += "Uses: " + row['Uses']
                    stats += '\n'
                    stats += row['Description']
                    unitembed.add_field(name='Item', value=stats, inline=False)
                if(row['Display Price'] == 'Yes'):
                    price = int(row['Uses']) * int(row['Price Per Use'])
                    price_string = str(price) + "G"
                    unitembed.add_field(name='Price: ', value=price_string, inline=False)
                await ctx.response.send_message(embed=unitembed)
                was_found = True
                break
        if (not was_found):
            await ctx.response.send_message("That item does not exist.")

def cc_get_ranks(row):
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

def cc_get_gains(row):
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
    if (row['Promotion Class 2'] != ''):
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
        if (row['Sword Gains 2'] != 'None' and row['Sword Gains 2'] != ''):
                gains4 += "<:RankSword:1083549037585768510>" + row['Sword Gains 2'] + " | "
        if (row['Lance Gains 2'] != 'None' and row['Lance Gains 2'] != ''):
                gains4 += "<:RankLance:1083549035622846474>" + row['Lance Gains 2'] + " | "
        """    if (row['Axe Gains 2'] != 'None'):
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
                gains4 += "<:RankDark:1083549034310012959>" + row['Dark Gains 2'] + " | " """
        if (len(gains4) > 0):
            gains4 = gains4[:-3]
        gains = gains + "\n" + gains3 + gains4
         
    return gains

def get_unit_names(ctx):
    names = ["Ellerie","Oriana","Tower","Pomelo","Lindros","Raylin","Reiker","Gecko","Mince","Yvette","Telon","Vermillion","Chalice","Oren","Nerysa","Dune","Murky","Krynia","Rohesia","Marlow","Whipjack","Francisca","Acielle","Qiulan","Guard","Tasel","Iosaf","Chixin","Thyme","Basil","Wisp","Foxberry","John XVI","Lilac","Ivadne","Xeo","Hagendire","Unari","Caloogo","Zububai","Sorbet","Aigo","Maurice","Joyful Jo","Empress","Helisent","Gil Goldfist","Avatar1","Avatar2","Avatar3","Avatar4","Avatar5","Betrayer","Justice","Lilac II","Afterimage"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

def get_item_names(ctx):
    names = ["Iron Sword","Steel Sword","Curved Sword","Crystal Sword","Silver Sword","Gold Sword","Umbral Edge","Brave Sword","Iron Blade","Steel Blade","Silver Blade","Wingcutter","Zanbato","Da Slasha","Lancereaver","Killing Edge","Rondel dagger","Cutlass","Rapier","Duan Dao","Chang Dao","Pocket Spell","Wind Sword","Bolt Sword","Flame Sword","Light Brand","Iron Lance","Steel Lance","Curved Lance","Crystal Lance","Silver Lance","Gold Lance","Umbral Lance","Brave Lance","Javelin","Short Spear","Spear","Wingpiercer","Heavy Spear","Da Stabba","Pitchfork","Harpoon","Axereaver","Killer Lance","Barrier Lance","Trident","Billhook","Iron Axe","Steel Axe","Curved Axe","Crystal Axe","Silver Axe","Gold Axe","Umbral Axe","Brave Axe","Hand Axe","Short Axe","Tomahawk","Halberd","Hammer","Da Smasha","Spellcleaver","Throwing Pick","Swordreaver","Killer Axe","Logsplitter","Shield Axe","Mansplitter","Iron Bow","Steel Bow","Crystal Bow","Silver Bow","Gold Bow","Umbral Bow","Brave Bow","Longbow","Greatbow","Titanbow","Spellbane","Da Shoota","Killer Bow","Shortbow","Incendiary Bow","Arcane Bow","Chu-ko-nu","Super Snipe","Breaking Point","Fireball","Sal's Surprise","Meteor","Bolgonone","Brud's Big Boom","Wind","Dicer of Dan","Blizzard","Tornado","Sick Sid's Slicer","Thunder","Woe of Joe","Bolting","Thoron","Ferion's Folly","Flux","Flux II","Moonglow","Flux VIII","Flux Alpha","Luna","Shell","Leech","Rupture","Ruin","Fortress","Nosferatu","Waste","Lightning","Shine","Purge","Divine","Aura","Torment","Lacerate","Obliterate","Cherish","Mindcrush","Scourge","Annihilate","Resire","Heal","Remedy","Heal More","Physic","Wave","Fortify","Silence","Skullsmash","Weaken","Sleep","Skinscourge","Guichen","Warp","Rescue","Envision","Hasten","Invigorate","Reinforce","Puolang","Badou","Bujie","Gaozhao","Chuanyang","Tianqian","Lingchi","Edict","Fancy Stabber","Seahawk Flag","Xonssuaencsy","Telescope","M. Widewater","Brutal Talon","Sharp Claw","Fleshpeeler","Piercing Bite","Crushing Bite","Vampire Fang","Ballista","Heavy Ballista","Elephant"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]