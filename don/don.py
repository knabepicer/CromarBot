import discord
import csv
import re
import random
from discord.ext import pages

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x085888)
    
    unitembed.set_thumbnail(url=row['Portrait'])
    
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    unitembed.add_field(name="Join Ch. ", value=row['Join Ch.'], inline=True)
    unitembed.add_field(name="Supports ", value=row['Supports'], inline=True)
    #unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Pow " + row['Pow'] + " | Skl " + row['Skl'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Mov'] + " | " + "Spd " + row['Spd']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Pow " + row['Pow Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "% | " + "Spd " + row['Spd Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = don_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotes'] == "Yes"):
        gains = don_get_gains(row)
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

def calculate_average_stats(row, level_string):
    """Calculate average stats for a unit at given level(s).
    Caps: 20 unpromoted (30 Luck, 60 HP), 30 promoted (30 Luck, 60 HP)."""
    level_parts = level_string.split('/')
    
    if len(level_parts) > 2:
        return None
    
    try:
        base_level = int(row['Lv'])
        base_stats = {
            'HP': int(row['HP']),
            'Pow': int(row['Pow']),
            'Skl': int(row['Skl']),
            'Spd': int(row['Spd']),
            'Luck': int(row['Luck']),
            'Def': int(row['Def']),
            'Res': int(row['Res'])
        }
        
        growths = {
            'HP': int(row['HP Growth']),
            'Pow': int(row['Pow Growth']),
            'Skl': int(row['Skl Growth']),
            'Spd': int(row['Spd Growth']),
            'Luck': int(row['Luck Growth']),
            'Def': int(row['Def Growth']),
            'Res': int(row['Res Growth'])
        }
        
        if len(level_parts) == 1:
            target_level = int(level_parts[0])
            levels_gained = target_level - base_level
            
            if levels_gained < 0:
                return None
            
            avg_stats = {}
            for stat in base_stats:
                avg_stats[stat] = base_stats[stat] + (growths[stat] / 100.0) * levels_gained
            
            # Apply unpromoted caps
            for stat in avg_stats:
                if stat == 'Luck':
                    avg_stats[stat] = min(avg_stats[stat], 30)
                elif stat == 'HP':
                    avg_stats[stat] = min(avg_stats[stat], 60)
                else:
                    avg_stats[stat] = min(avg_stats[stat], 20)
            
            return {
                'stats': avg_stats,
                'description': f"Level {target_level}",
                'class_name': row['Class']
            }
        
        else:
            unpromoted_level = int(level_parts[0])
            promoted_level = int(level_parts[1])
            
            unpromoted_levels = unpromoted_level - base_level
            if unpromoted_levels < 0:
                return None
            
            promoted_levels = promoted_level - 1
            if promoted_levels < 0:
                return None
            
            stats_at_promotion = {}
            for stat in base_stats:
                stats_at_promotion[stat] = base_stats[stat] + (growths[stat] / 100.0) * unpromoted_levels
            
            # Apply unpromoted caps before promotion
            for stat in stats_at_promotion:
                if stat == 'Luck':
                    stats_at_promotion[stat] = min(stats_at_promotion[stat], 30)
                elif stat == 'HP':
                    stats_at_promotion[stat] = min(stats_at_promotion[stat], 60)
                else:
                    stats_at_promotion[stat] = min(stats_at_promotion[stat], 20)
            
            promotion_gains = {
                'HP': int(row['HP Gains']) if row['HP Gains'] else 0,
                'Pow': int(row['Pow Gains']) if row['Pow Gains'] else 0,
                'Skl': int(row['Skl Gains']) if row['Skl Gains'] else 0,
                'Spd': int(row['Spd Gains']) if row['Spd Gains'] else 0,
                'Def': int(row['Def Gains']) if row['Def Gains'] else 0,
                'Res': int(row['Res Gains']) if row['Res Gains'] else 0,
                'Luck': 0
            }
            
            for stat in stats_at_promotion:
                stats_at_promotion[stat] += promotion_gains[stat]
            
            avg_stats = {}
            for stat in stats_at_promotion:
                avg_stats[stat] = stats_at_promotion[stat] + (growths[stat] / 100.0) * promoted_levels
            
            # Apply promoted caps
            for stat in avg_stats:
                if stat == 'Luck':
                    avg_stats[stat] = min(avg_stats[stat], 30)
                elif stat == 'HP':
                    avg_stats[stat] = min(avg_stats[stat], 60)
                else:
                    avg_stats[stat] = min(avg_stats[stat], 30)
            
            promotion_class = row['Promotion Class'] if row['Promotion Class'] else "Promoted"
            
            return {
                'stats': avg_stats,
                'description': f"Level {unpromoted_level}/{promoted_level}",
                'class_name': promotion_class
            }
    
    except (ValueError, KeyError):
        return None

def get_averaged_stats_embed(row, level_string):
    """Create an embed showing averaged stats."""
    result = calculate_average_stats(row, level_string)
    
    if result is None:
        return None
    
    stats = result['stats']
    
    embed = discord.Embed(
        title=f"{row['Name']} {row['Affinity']} - {result['description']}", 
        color=0x085888
    )
    embed.set_thumbnail(url=row['Portrait'])
    embed.add_field(name="Class", value=result['class_name'], inline=True)
    
    avg_bases = (f"HP {stats['HP']:.1f} | "
                 f"Pow {stats['Pow']:.1f} | "
                 f"Skl {stats['Skl']:.1f} | "
                 f"Lck {stats['Luck']:.1f} | "
                 f"Def {stats['Def']:.1f} | "
                 f"Res {stats['Res']:.1f} | "
                 f"Spd {stats['Spd']:.1f}")
    
    embed.add_field(name="Average Stats", value=avg_bases, inline=False)
    
    return embed




async def unit(ctx, name: str, levels: str = None):
    """Display unit data. Optionally calculate average stats at a given level."""
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('don/doubled_unit.csv', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                was_found = True
                
                if levels is not None:
                    embed = get_averaged_stats_embed(row, levels)
                    if embed is None:
                        await ctx.response.send_message(
                            "Invalid level format. Use format like `10` or `10/5`."
                        )
                    else:
                        await ctx.response.send_message(embed=embed)
                else:
                    paginator = pages.Paginator(pages=get_unit_pages(row), show_menu=True, show_disabled=False, show_indicator=False, menu_placeholder="Select page to view", timeout =120, disable_on_timeout = True)
                    await paginator.respond(ctx.interaction)
                break
        if (not was_found):
            await ctx.response.send_message("That unit does not exist.")

async def item(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)            
    with open('don/doubled_item.csv', newline='', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            was_found = False
            for row in reader:
                if(row['Name'].lower() == stripped_name.lower()):
                    unitembed=discord.Embed(title=row['Display Name'], color=0x085888)
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



def don_get_ranks(row):
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

def don_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != '0'):
        gains += "HP: +" + row['HP Gains'] + " | "
    if (row['Pow Gains'] != '0'):
        gains += "Pow: +" + row['Pow Gains'] + " | "
    if (row['Skl Gains'] != '0'):
        gains += "Skl: +" + row['Skl Gains'] + " | "
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
    if (row['Spd Gains'] != '0'):
        gains += "Spd: +" + row['Spd Gains'] + " | "
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
    names = ["Marion","Puzon","Kiwi","Crys","Verona","Kalores","Raeford","Simon","Otto","Thoril","Lass","Andreas","Tobias","Polyph"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

def get_item_names(ctx):
    names = ["Iron Sword","Slim Sword","Steel Sword","Silver Sword","Iron Blade","Steel Blade","Quick Sword","Knaveknife","Lunar Knife","Titan's Knife","Devil's Dagger","Brave Sword","Mercurius","Killing Edge","Shamshir","Armorslayer","Zanbato","Wyrmslayer","Light Brand","Runesword","Lancereaver","Sunrise Bld.","Sunrise Bld.","Brave Blade","Sealed Blade","Iron Lance","Slim Lance","Steel Lance","Silver Lance","Quick Lance","Troop Lance","Brave Lance","Killer Lance","Ridersbane","Ridersbane","Hexlocker","Javelin","Short Spear","Spear","Axereaver","Axeslayer","Iron Axe","Slim Axe","Steel Axe","Silver Axe","Quick Axe","Brave Axe","Fiend's Cleaver","Mystic Axe","Killer Axe","Halberd","Hammer","Dragon Axe","Devil Axe","Hand Axe","Short Axe","Tomahawk","Bolthammer","Swordreaver","Swordslayer","Iron Bow","Slim Bow","Steel Bow","Silver Bow","Quick Bow","Reverie Bow","Reverie Bow","Killer Bow","Brave Bow","Close Draw","Spell's Bane","Longbow","Shortshot","Ballista","Blue Swallow","Fire","Thunder","Blizzard","Bolting","Bolganone","Dying Blaze","Levianeer","Light","Light","Shine","Divine","Resire","Purge","Guardian","Bragi's Blight","Flux","Luna","Omen","Jormungand","Eclipse","Fenrir","Upheaval","Gnipahellir","Shadow Bolt","Evil Eye","Glower Eye","Farsight","Heal","Mend","Physic","Silence","Sleep","Rescue","Hammerne","Barrier","Angelic Robe","Energy Ring","Secret Book","Speedwing","Dragonshield","Brittle Ring","Flimsy Band","Eerie Charm","Wing Statue","Iron Rune","Null Guard","Rotten Claw","Firestone","Icestone","Magestone","Chest Key","Door Key","Vulnerary","Elixir","Pure Water","Light Rune","Master Seal","Leader's Rite","Jewel of Fire","Jewel of Fire","Stone Scroll"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
