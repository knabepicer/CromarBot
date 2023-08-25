import discord
import csv
import re
import random
from discord.ext import commands
from discord import option


async def unit(ctx, name: str):
    with open('bob/bob unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            if(row['Name'].lower() == name.lower()):
                #await interaction.response.send_message("Name: " + row["Name"] + " HP Growth:" + row["HP Growth"])
                unitembed=discord.Embed(title=name.capitalize(), color=0xac6c6c)
                if (name.lower() == 'cromar' and random.randint(1, 10) == 1):
                    unitembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1043928901610643456/1080640506473762927/CromarFoggingOutknabepicer_1_1.png')
                    unitembed.add_field(name="Lv " + row['Lv'] + " ", value='Slayer', inline=True)
                elif (name.lower() == 'sera' and random.randint(1,10) == 1):
                    unitembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1043928901610643456/1080644681379106846/SeraZoomingRozeknabepicer_1.png')
                    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
                else:
                    unitembed.set_thumbnail(url=row['Portrait'])
                    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
                
                unitembed.add_field(name="PCC: ", value=row['PCC'], inline=True)
                unitembed.add_field(name="Movement Stars: ", value=row['Vigor'], inline=True)
                unitembed.add_field(name="Leadership: ", value=row['Leadership'], inline=True)
                bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] + " | " + "Mag " + row['Mag']+ " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Bld " + row['Bld'] + " | " + "Mov " + row['Mov']
                unitembed.add_field(name="Bases", value=bases, inline=False)
                growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | " + "Mag " + row['Mag Growth']+ "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "% | " + "Bld " + row['Bld Growth'] + "% | Mov " + row['Mov Growth'] + "%"
                unitembed.add_field(name="Growths", value=growths, inline=False)
                ranks = bob_get_ranks(row)
                unitembed.add_field(name="Ranks", value=ranks, inline=False)
                if (row['Skills'] != "None"):
                    unitembed.add_field(name="Skills", value=row['Skills'], inline=False)
                if (row['Promotes'] == "Yes"):
                    gains = bob_get_gains(row)
                    unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
                await ctx.response.send_message(embed=unitembed)
                was_found = True
                break
        if (not was_found):
            await ctx.response.send_message("That unit does not exist.")


async def item(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    if (stripped_name.lower() == 'axle'):
        await ctx.response.send_message("For Axel's Axle, search 'Axle1'. For Alex's Axle, search 'Axle2'.")  
    else:             
        with open('bob/bob item.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            was_found = False
            for row in reader:
                if(row['Name'].lower() == stripped_name.lower()):
                    unitembed=discord.Embed(title=row['Display Name'], color=0xac6c6c)
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

async def skill(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('bob/bob skill.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                unitembed=discord.Embed(title=row['Name'], color=0xac6c6c)
                unitembed.add_field(name='Description: ', value=row['Description'], inline=False)
                was_found = True
                await ctx.response.send_message(embed=unitembed)
                break
        if (not was_found):
                await ctx.response.send_message("That skill does not exist.")

def bob_get_ranks(row):
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

def bob_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
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
    if (row['Bld Gains'] != '0'):
        gains += "Bld: +" + row['Bld Gains'] + " | "
    if (row['Mov Gains'] != '0'):
        gains += "Mov: +" + row['Mov Gains'] + " | "
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
    return gains

def get_unit_names(ctx):
    names = ["Cleo","Mira","Iskra","Emil","Svetomir","Alena","Varga","Delilah","Alex","Axel","Filone","Zwieback","Leina","Cromar","Loewe","Longxia","Fangai","Mish","Tobie","Awa","Cadenza","Faolan","Iberis","Buldak","Nora","Hans","Takai","Jenny","Meldan","Valse","Hornet","Milo","Ichwep","Mink","Tiberius","Ellerey","Mantou","Tippany","Pelecaye","Carl","Darby","Jacinth","Nahiza","Augur","Ilse","Rashid","Nikolas","Sera","Shaw","Apsis","Ojasvi","Joie","Groto","Tao","Zhara","Volran","Tara","Jerry","Lyre","Ngondala","Catrin","Matthias","Kwame","Kofi","Trajan","Locke","Elias","Boro","Orfeas","Barod","Taraji","Athan","Asha","Dragana","Athanasius","Kailani","Korovai","Radnitz","Coralia"]
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

def get_item_names(ctx):
    names = ["Iron Sword","Slim Sword","Steel Sword","Silver Sword","Iron Blade","Longsword","Greatsword","Flame Sword","Rapier","Short Sword","Brave Sword","King Sword","Killing Edge","Armorslayer","Paragon Sword","Thunder Sword","Wind Sword","Sleep Sword","Master Sword","Iron Lance","Slim Lance","Steel Lance","Silver Lance","Short Lance","Brave Lance","Killer Lance","Horseslayer","Javelin","Long Lance","Great Lance","Iron Axe","Steel Axe","Silver Axe","Berserk Sword","Brave Axe","Killer Axe","Poleaxe","Hammer","Devil Axe","Hand Axe","Master Axe","Master Lance","Shortbow","Greatbow","Iron Bow","Steel Bow","Silver Bow","Master Bow","Killer Bow","Brave Bow","Bolganone","Longbow","Long Arch","Iron Arch","Killer Arch","Fire","Thunder","Elfire","Bolting","Thoron","Wind","Tornado","Lightning","Blizzard","Nosferatu","Purge","Aura","Again","Flux","Sigil","Jormungand","Fenrir","Hel","Meteor","Heal","Mend","Maharaghi","Physic","Fortify","Restore","Silence","Sleep","Berserk","Warp","Rescue","Torch","Hammerne","Unlock","Barrier","Rewarp","Angelic Robe","Energy Ring","Secret Book","Speedwings","Goddess Icon","Dragonshield","Talisman","Swiftsoles","Body Ring","Slim Bow","Devil's Dagger","Ballad Of War","The Breaker","Muramasa","Chest Key","Door Key","Vulnerary","Elixir","Pure Water","Spirit Dust","Torch","Thief","Member Card","White Gem","Blue Gem","Red Gem","Kaiserschwert","Light Rune","Stone Sword","Ice Sword","Argilabrys","Tempered Ring","Civilian Proof","Battle Axe","Lumen","Knight Proof","Wind Bow","Fire Drive","Slim Arch","Stinger","Mystic Lance","Lunar Axe","Stormbrand","Darkbrand","Hounding Bow","Daybreak","Heavy Spear","Holyspear","Crusher","Argymos Crest","Crowned Pyre","Stormbreaker","Absolute Zero","Eye of Dawn","Faith's Wind","Dancing Blade","Bone Club","Taodao","Rune Arrow","Black Anklet","Boltbrand","Dawn Pendant","Dragonstone","Unmoor","Impaler","Nibiru","Zykhra Scroll","Beiyr Scroll","Raio Scroll","Luzen Scroll","Cherne Scroll","Dreedur Scroll","Worn Scroll","Amser Scroll","Firestone","Marksman Bow","Claymore","Slim Axe","Azurium","Gale Bow","Dullahan","Burn","Counter Bow","Conversion","Ritual Knife","Brenthunder","Spell Mirror","Arai's Gale","Arai's Gale","Sister Ring","Hurlbat","Arachnid","Yor's Yari","Break Arc","Meat Cleaver","Axle1","Axle2","Miaodao","King Shield","Edged Arrow","Red Scarf","Saunion","Trained Edge","Trained Pike","Trained Axe","Trained Arc","Aqua Brand","Charge","Archival","Sink","Woodlands Huke","Captains Helm","Fealty Bow","Lamfada","Bold Blade","Bold Pike","Bold Cleaver","Luna","Earth Greataxe","Runespear","Fang And Claw","Starcutter","Full Helm","Blade Crusher","Shieldbearer","Malkhut","Sagittae","Kukri","Slam Brace","Zweihander","Deadeye Bow","Moonlight Blade","Glaive","Predestination","Titan's Fang","Svarog","Worldcleaver","Indra","Agni","Smoldering Seal","Apotheosis","Byelen's Bell","Ragnarok","Kali Yuga","Armageddon"]
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

def get_skill_names(ctx):
    names = ["Steal","Vantage","Locktouch","Adept","Astra","Charisma","Wrath","Paragon","Desperation","Hex","Even Rhythm","Odd Rhythm","Dazzle","Reposition","Rally Defense","Rally Resistance","Savior","Certain Blow","Savage Blow","Renewal","Pass","Swap","Shove","Smite","Provoke","Imbue","Armored Blow","Critical Force","Dance","Life and Death","Lifetaker","BowRange+1","Acrobat","Battle Veteran","Nullify","Fortune","Breath Of Life","Shade","Opportunist","Puissance","Death Blow","Radiance","Nightcaller","Avenger","Reckless Charge","Aftershock","Headshot","Culling","Bargain","Watchful","Noncombatant","Gladiator's Aura","Azurium Might","Alacrity","Sharpshooter","Desolate","Spur Hit","Blade Dance","Absolute Zero","Crowned Pyre","Eye Of Dawn","Faith's Wind","Stormbreaker","Spelltwister","Telepathy","Adrenaline Rush!!","Decian Fealty","Dragon Rage","Piercing Bolt","Flight"]
    return [name for name in names if name.lower().startswith(ctx.value.lower())]