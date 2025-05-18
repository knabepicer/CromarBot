import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x7c00c9)
    #supportembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x34c290)
    unitembed.set_thumbnail(url=row['Portrait'])
    #supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] + " | " + "Mag " + row['Mag'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Mov']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | " + "Mag " + row['Mag Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = oc_get_ranks(row)
    unitembed.add_field(name="Skills", value=row['Skills'], inline=False)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotion Class'] != ""):
        gains = oc_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    if (row['Bonus'] != ''):
        unitembed.set_footer(text="Unit also has access to: " + row['Bonus'])
    
    
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
    with open('oc/oc_unit.csv', newline='', encoding="utf-8-sig") as csvfile:
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
async def item(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)            
    with open('oc/oc_item.csv', newline='', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            was_found = False
            for row in reader:
                stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
                if(stripped_row.lower() == stripped_name.lower()):
                    unitembed=discord.Embed(title=row['Display Name'], color=0x7c00c9)
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
                    if(row['Display Price'] == 'Yes'):
                        price = int(row['Uses']) * int(row['Price Per Use'])
                        price_string = str(price) + "G"
                        unitembed.add_field(name='Price: ', value=price_string, inline=False)
                    await ctx.response.send_message(embed=unitembed)
                    was_found = True
                    break
            if (not was_found):
                await ctx.response.send_message("That item does not exist.")


def oc_get_ranks(row):
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

def oc_get_gains(row):
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
    if (row['Promotion Skills'] != 'None'):
         gains2 += "\n" + row['Promotion Skills']
    gains2 += '\n'
    gains3 = ""
    gains4 = ""
    if (row['Promotion Class 2'] != ''): 
        gains3 += '\n' + row['Promotion Class 2'] + '\n'
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
        if (len(gains3) > 0):
            gains3 = gains3[:-3]
        gains3 += '\n'
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
        if (len(gains4) > 0):
            gains4 = gains4[:-3]
        if (row['Promotion Skills 2'] != 'None'):
            gains4 += "\n" + row['Promotion Skills 2']
        
        
    return gains + gains2 + gains3 + gains4

def get_unit_names(ctx):
    names = ["Matthew","Melina","Emily","Yukiko","Labrys","Rickson","Violet","Diana","Elowyn","Skye","Yuro","Rosalyn","Salazar","Safira","Ashley","Tarif","Kirk","Selpan","Eirika","Manok","Koryn","Hikari","Aries","Leonid","Reggie","Killian","Elsbeth","Valentin","Khix","Krielle","Emiko","Judmila","Esera","Alexis","Martin","Nadia","Nikana","Ashiya","Seimei","Stephen","Nalim","Selene","Sirianne","Waffles","Lizabel","Artemis","Valentina","Amy","Kay"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

""" def get_skill_names(ctx):
    names = ["Charisma","Pass","Nihil","Gentilhomme","Miracle","Light Weight","Swap","Strong Riposte","Wrath","Spur Resistance","Bond","Quick Burn","Intimidate","Savior","Reposition","Spur Strength","Pivot","Knight Aspirant","Slow Burn","Acrobat","Vantage","Spur Magic","Darting Blow","Thunderstorm","Puissance","Demoiselle","Charm","Spur Speed","Spur Defense","Summon","Paragon","Hex","Pursuit","Heavy Strikes","Inspiration","Lily's Poise","Chivalry","Pragmatic","Anathema","Death Blow","Boon","Armored Blow","Perfectionist","Fiery Blood","Even Rhythm","Frenzy","Triangle Adept","Tantivy","Nullify","Duelist's Blow","Odd Rhythm","Vanity","Infiltrator","Opportunist","Relief","Desperation","Staff Savant","Shove","Quick Draw","Natural Cover","Cunning","Steal","Crit Boost","Certain Blow","Forager","Discipline+","Live to Serve","Locktouch","Steal+","Breath of Life","Wind Disciple","Voice of Peace","Camaraderie"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())] """

def get_item_names(ctx):
    names = ["Chaos Breath", "Iron Sword","Steel Sword","Mythril Sword","Diamond Sword","Ancient Sword","Boomerang","Q-Merang","Killing Edge","Cold Sword","Lancereaver","Wyrmslayer","Kampilan","Iron Lance","Steel Lance","Mythril Lance","Diamond Shovel","Ancient Lance","Javelin","Yamato Spear","Killer Lance","Fire Lance","Axereaver","Ridersbane","Iron Axe","Steel Axe","Mythril Axe","Diamond Axe","Ancient Axe","Hand Axe","Tomahawk","Killer Axe","Bolt Axe","Swordreaver","Hammer","Daedric Axe","Iron Bow","Steel Bow","Mythril Bow","Ancient Bow","Gale Bow","Crossbow","Longbow","Longerbow","Longestbow","Musket","Machine Gun","Mega Buster","Laser Gun","Arrowspate","Hoistflamme","Thunderbolt","Cob Cannon","Elephant","Flames","Frostbite","Sparks","Fireball","Tri Attack","Bombos","Ether","Quake","Thunderstorm","Blizzard","Photon","Belmont","Stendarr","Banish","Meridia","Talos","Flux","D'Void","Nosferatu","Vaermina","Maleficent","Nothebis","Mehrunes","Heal","Mend","Recover","Physic","Pizza Time","Esuna","Byrna Cane","Fire Rod","Ice Rod","Lightning Rod","Somaria Cane","Pacci Cane","Unlock","Icestone","Firestone","Magestone","Earthstone","Unrelenting Force","Ice Form","Dragonrend","Basic Tie","Cone Helm","Bucket Helm","Knight Helm","Rock Core","Ice Core","Steel Core","Ancient Beam","Charm Ray","Freeze Ray","Enervation Ray","Telekinesis","Disintegration","Death Ray","Stone","Ray of Frost","FierySaber","Hookshot","Freeze-Dry","Gauldur Blade","Chainsaw","Amihan","Habagat","Ramuh","Dunblade","Levin Sword","Flameblade","Mispell Blade","Monado","Master Sword","Neapolisword","Lightsaber","Arectaris","Reginleif Plus","Mjölnir","Rocket Bow","Seven Scimitar","Adamant","Lustrous","Gemini Laser","Axe Launcher","Scorching Ray","Neapolibeam","Bagpipes","Amagidyne","Neuroshock","Solar Flare","Brainshock","Meteor","Wabbajack","Divinestone","Ascalon","Keening","Bitter Mercy","Pugi","Sunder","Griseous","Cryolator","Excalipoor","Shí Huán","Vishanti","Darkhold","Hammerne","Centrifuge","Warp","Rescue","Wraithguard","Bread","Nuggets","Ice Cream","Milk","Sweet Roll","Chocolate Milk","Burger Meal","Wall Poultry","Milkshake","Cake","Door Key","Chest Key","Lockpick","Potato Mine","Plantern","Diploma","Heart Crystal","Power Beans","Charm of Bezel","Fanfics","Cheese","Icosahedron","Wall-Nut","Chocolate Bar","Minecart","Sandvich","Super Serum","Gold Ingot","Ruby","Emerald","Diamond","Platinum","Delta Shield","Smogon Seal","Oro Card","Metro Card","Ninis's Grace","Hela's Wrath","Thor's Ire","Loki's Mischief","Dwemer Gyro","Zeal Machine","Sheikah Core","Agarthan UI","Sub-Energy","El Vibrato Key","DNA Extractor","Atlantean Gem","40m/s Gauge","Arc Reactor","Reality Stone","Soul Stone","Mind Stone","Time Stone","Space Stone","Power Stone"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

