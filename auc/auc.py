import discord
import csv
import re
import random
from discord.ext import pages

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x4e3ca3)
   # supportembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x4e3ca3)
    unitembed.set_thumbnail(url=row['Portrait'])
    #supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    unitembed.add_field(name="Join Ch. ", value=row['Join Ch.'], inline=True)
    if (row['Supports'] != "None"):
        unitembed.add_field(name='Supports', value=row['Supports'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Pow " + row['Pow'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Mov']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Pow " + row['Pow Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = auc_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotes'] == "Yes"):
        gains = auc_get_gains(row)
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
  
    return page_groups


#cota = cromar.create_subgroup("cota", "Get Call of the Armor data")

async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('auc/auc_unit.csv', newline='' , encoding="utf-8-sig") as csvfile:
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
    with open('auc/auc_item.csv', newline='', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            was_found = False
            for row in reader:
                if(row['Name'].lower() == stripped_name.lower()):
                    unitembed=discord.Embed(title=row['Display Name'], color=0x4e3ca3)
                    unitembed.set_thumbnail(url=row['Icon'])
                    if(row['Type'] == 'Weapon'):
                        stats = "Rank: " + row['Weapon Level'] + " | Mt: " + row['Mt'] + " | Hit: " + row['Hit'] + " | Crit: " + row['Crit'] + " | Wt: " + row['Wt'] + " | Range: " + row['Range'] + " | WEXP: " + row['WEXP']
                        if (row['Uses'] == '255'):
                            stats += " | Unbreakable"
                        else:
                            stats += " | Uses: " + row['Uses']
                        if (row['Description'] != "None"):
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
                    await ctx.response.send_message(embed=unitembed)
                    was_found = True
                    break
            if (not was_found):
                await ctx.response.send_message("That item does not exist.")


def auc_get_ranks(row):
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

def auc_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != '0'):
        gains += "HP: +" + row['HP Gains'] + " | "
    if (row['Pow Gains'] != '0'):
        gains += "Pow: +" + row['Pow Gains'] + " | "
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
            gains += "<:RankSword:1083549037585768510>+" + row['Sword Gains'] + " | "
        else:
            gains += "<:RankSword:1083549037585768510>" + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
        if (row['Lance Gains'].isdigit()):
            gains += "<:RankLance:1083549035622846474>+" + row['Lance Gains'] + " | "
        else:
            gains += "<:RankLance:1083549035622846474>" + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
        if (row['Axe Gains'].isdigit()):
            gains += "<:RankAxe:1083549032292548659>+" + row['Axe Gains'] + " | "
        else:
            gains += "<:RankAxe:1083549032292548659>" + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
        if (row['Bow Gains'].isdigit()):
            gains += "<:RankBow:1083549033429205073>+" + row['Bow Gains'] + " | "
        else:
            gains += "<:RankBow:1083549033429205073>" + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
        if (row['Staff Gains'].isdigit()):
            gains += "<:RankStaff:1083549038936326155>+" + row['Staff Gains'] + " | "
        else:
            gains += "<:RankStaff:1083549038936326155>" + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
        if (row['Anima Gains'].isdigit()):
            gains += "<:RankAnima:1083549030598049884>+" + row['Anima Gains'] + " | "
        else:
            gains += "<:RankAnima:1083549030598049884>" + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
        if (row['Light Gains'].isdigit()):
            gains += "<:RankLight:1083549037019541614>+" + row['Light Gains'] + " | "
        else:
            gains += "<:RankLight:1083549037019541614>" + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
        if (row['Dark Gains'].isdigit()):
            gains += "<:RankDark:1083549034310012959>+" + row['Dark Gains'] + " | "
        else:
            gains += "<:RankDark:1083549034310012959>" + row['Dark Gains'] + " | "
    gains = gains[:-3]
    if (row['Promotes 2'] != 'No'): 
        gains += '\n' + row['Promotion Class 2'] + '\n'
        if (row['HP Gains 2'] != '0'):
            gains += "HP: +" + row['HP Gains 2'] + " | "
        if (row['Pow Gains 2'] != '0'):
            gains += "Pow: +" + row['Pow Gains 2'] + " | "
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
                gains += "<:RankSword:1083549037585768510>+" + row['Sword Gains 2'] + " | "
            else:
                gains += "<:RankSword:1083549037585768510>" + row['Sword Gains 2'] + " | "
        if (row['Lance Gains 2'] != 'None'):
            if (row['Lance Gains 2'].isdigit()):
                gains += "<:RankLance:1083549035622846474>+" + row['Lance Gains 2'] + " | "
            else:
                gains += "<:RankLance:1083549035622846474>" + row['Lance Gains 2'] + " | "
        if (row['Axe Gains 2'] != 'None'):
            if (row['Axe Gains 2'].isdigit()):
                gains += "<:RankAxe:1083549032292548659>+" + row['Axe Gains 2'] + " | "
            else:
                gains += "<:RankAxe:1083549032292548659>" + row['Axe Gains 2'] + " | "
        if (row['Bow Gains 2'] != 'None'):
            if (row['Bow Gains 2'].isdigit()):
                gains += "<:RankBow:1083549033429205073>+" + row['Bow Gains 2'] + " | "
            else:
                gains += "<:RankBow:1083549033429205073>" + row['Bow Gains 2'] + " | "
        if (row['Staff Gains 2'] != 'None'):
            if (row['Staff Gains 2'].isdigit()):
                gains += "<:RankStaff:1083549038936326155>+" + row['Staff Gains 2'] + " | "
            else:
                gains += "<:RankStaff:1083549038936326155>" + row['Staff Gains 2'] + " | "
        if (row['Anima Gains 2'] != 'None'):
            if (row['Anima Gains 2'].isdigit()):
                gains += "<:RankAnima:1083549030598049884>+" + row['Anima Gains 2'] + " | "
            else:
                gains += "<:RankAnima:1083549030598049884>" + row['Anima Gains 2'] + " | "
        if (row['Light Gains 2'] != 'None'):
            if (row['Light Gains 2'].isdigit()):
                gains += "<:RankLight:1083549037019541614>+" + row['Light Gains 2'] + " | "
            else:
                gains += "<:RankLight:1083549037019541614>" + row['Light Gains 2'] + " | "
        if (row['Dark Gains 2'] != 'None'):
            if (row['Dark Gains 2'].isdigit()):
                gains += "<:RankDark:1083549034310012959>+" + row['Dark Gains 2'] + " | "
            else:
                gains += "<:RankDark:1083549034310012959>" + row['Dark Gains 2'] + " | "
        gains = gains[:-3]
    return gains


def get_unit_names(ctx):
    names = ["Puzon","Teodor","Wil","Isadora","Garcia","Groznyi","Wire","Dorothy","Yodel","Lugh","Chad","Erik","Farina","Sophia","Hawkeye","Limstella","Selena","Amelia","Uhai","Marisa","Ein","Lucius","Raven","Renault","Zeiss","Fargus","Wallace","Dara","William","Denning","Ephraim","Eirika","Thany","Duessel","Pablo","Nils","Karla","Leila","Beran","Knoll","Ursula","Caelin","Sigune","Sonia","Roy","Myrrh","Lance","Kyle","Cath","Jerme","Hugh","Lyon","Athos","Valter","Jan","Bartre","Echidna","Linus","Lloyd","L'Arachel","Sue","Elen","Milady","Eliwood","Iduun","Eleanora","Nergal"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

def get_item_names(ctx):
    names = ["Iron Sword","Slim Sword","Steel Sword","Silver Sword","Iron Blade","Steel Blade","Silver Blade","Poison Sword","Gale Blade","Rapier","Noble Rapier","Dirk","Glaurung","Brave Sword","Regal Blade","Regale Blade","Killing Edge","Wo Dao","Goujian","Rune Blade","Mani Katti","Sol Katti","Binding Blade","Durandal","Armorslayer","Zanbato","Zanbato","Wyrmslayer","Magebane","Light Brand","Wind Sword","Flame Blade","Runesword","Lunar Blade","Lancereaver","Zweihander","Oni Katti","Deus Katti","Iron Lance","Slim Lance","Steel Lance","Silver Lance","Heartpiercer","Military Fork","Brave Lance","Killer Lance","Heavy Spear","Ridersbane","Ridersbane","Knightkneeler","Dragonpike","Duren's Spear","Feimazuo Dao","Javelin","Short Spear","Spear","Vaida's Spear","Rose of War","Nibelung","Axereaver","Reginleif","Saunion","Pilum","Iron Axe","The Iron Axe","Slim Axe","Steel Axe","Silver Axe","Battle Axe","Wolf Beil","Armads","Brave Axe","Raionos","Basilikos","Enduring Soul","Elimine Axe","Elimine Axe","Killer Axe","Halberd","Hammer","Dragon Axe","Devil Axe","Hand Axe","Short Axe","Tomahawk","Hatchet","Swordreaver","Swordslayer","Ax o' The Titan","Ax o' The Titan","Iron Bow","Short Bow","Steel Bow","Silver Bow","Poison Bow","Delphi","Skadi","Killer Bow","Brave Bow","Moonbow","Swiftshot","Spellseal Bow","Spellseal Bow","Longbow","Greatbow","Hwatcha","Ballista","Iron Ballista","Whale Hunter","Kraken Hunter","Fire","Thunder","Elfire","Bolting","Fimbulvter","Aircalibur","Cleanse","Shock Burst","Airblade","Forblaze","Lightning","Lightning","Shine","Divine","Thani","Purge","Aura","Morphic Dirge","Piety","Star Burst","Ivaldi","Flux","Luna","Malaise","Nosferatu","Eclipse","Fenrir","Ereshkigal","Shadow Shrike","Gespenst","Moon Burst","Munio","Heal","Mend","Recover","Poultice","Relaxing Melody","Physic","Darkmend","Fortify","Latona","Restore","Refreshing Herb","Silence","Sleep","Dissonant Chord","Rescue","Warp","Torch","Hammerne","Unlock","Barrier","Demon Light","Firestone","Icestone","Magestone","Earthstone","Dragonstone","Divinestone","Shadowstone","Firestone X","Wretched Air","Angelic Robe","Energy Ring","Secret Book","Speedwing","Goddess Icon","Dracoshield","Talisman","Body Ring","Boots","Metis's Tome","Member Card","Hoplon Guard","Fili Shield","Teal Gem","Red Gem","Blue Gem","Gold Gem","Chest Key","Chest Key","Chest Key (5)","Door Key","Master Key","Vulnerary","Vulnerary (60)","Elixir","Pure Water","Torch","Light Rune","Hero Crest","Knight Crest","Orion's Bolt","Elysian Whip","Guiding Ring","Ocean Seal","Heaven Seal","Master Seal","Caller Seal","Filla's Might","Sake","Eduardo's Ring","Jewel of Fire","Jewel of Fire","Ancient Scale","Fire Emblem"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]