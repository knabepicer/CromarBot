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
    
    
    summonfound = False
    with open('auc/auc_summon.csv', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for summonrow in reader:
            if(row['Name'] == summonrow['Summoner Name']):
                summonembed=discord.Embed(title=summonrow['Summon Name'] + " " + summonrow['Affinity'], color=0x4e3ca3)
                summonembed.add_field(name="Lv " + summonrow['Lv'] + " ", value=summonrow['Class'], inline=True)
                summonbases = "HP " + summonrow['HP'] + " | " + "Pow " + summonrow['Pow'] + " | Skl " + summonrow['Skl'] + " | " + "Spd " + summonrow['Spd'] + " | " + "Lck " + summonrow['Luck'] + " | " + "Def " + summonrow['Def'] + " | " + "Res " + summonrow['Res'] + " | " + "Con " + summonrow['Con'] + " | " + "Mov " + summonrow['Mov']
                summonembed.add_field(name="Bases", value=summonbases, inline=False)
                summongrowths = "HP " + summonrow['HP Growth'] + "% | " + "Pow " + summonrow['Pow Growth'] + "% | Skl " + summonrow['Skl Growth'] + "% | " + "Spd " + summonrow['Spd Growth'] + "% | " + "Lck " + summonrow['Luck Growth'] + "% | " + "Def " + summonrow['Def Growth'] + "% | " + "Res " + summonrow['Res Growth'] + "%"
                summonembed.add_field(name="Growths", value=summongrowths, inline=False)
                summonranks = auc_get_ranks(summonrow)
                summonembed.add_field(name="Ranks", value=summonranks, inline=False)
                stats = summonrow['Weapon Type'] + "\n" + "Mt: " + summonrow['Weapon Mt'] + " | Hit: " + summonrow['Weapon Hit'] + " | Crit: " + summonrow['Weapon Crit'] + " | Wt: " + summonrow['Weapon Wt'] + " | Range: " + summonrow['Weapon Rng']
                stats += " | Unbreakable"
                if (summonrow['Description'] != "None"):
                    stats += '\n'
                    stats += summonrow['Description']
                summonembed.add_field(name=summonrow['Weapon Name'], value=stats, inline=False)

                summonfound = True
                break
   
    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        ),
       
        
    ]
    if (summonfound):
        page_groups.append(pages.PageGroup
        (
        pages=[summonembed],
        label="Summon",
        description="Data on this character's summoned unit",
        use_default_buttons=False,
        )
        )
  
    return page_groups

def calculate_average_stats(row, level_string):
    """
    Calculate average stats for a unit at given level(s).
    Supports up to 3 tiers for units that can promote twice.
    Applies stat caps: 20 unpromoted (30 for Luck), 30 promoted.
    
    Args:
        row: CSV row containing unit data
        level_string: String in format "10", "10/5", or "10/10/5"
    
    Returns:
        Dictionary with calculated stats, or None if invalid input
    """
    # Parse the level string
    level_parts = level_string.split('/')
    
    if len(level_parts) > 3:
        return None  # Invalid format
    
    try:
        # Get base level and stats
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
        
        # Get growth rates (as percentages)
        growths = {
            'HP': int(row['HP Growth']),
            'Pow': int(row['Pow Growth']),
            'Skl': int(row['Skl Growth']),
            'Spd': int(row['Spd Growth']),
            'Luck': int(row['Luck Growth']),
            'Def': int(row['Def Growth']),
            'Res': int(row['Res Growth'])
        }
        
        # Calculate based on number of level segments
        if len(level_parts) == 1:
            # Simple case: just one level value (unpromoted)
            target_level = int(level_parts[0])
            levels_gained = target_level - base_level
            
            if levels_gained < 0:
                return None  # Can't go below base level
            
            # Calculate average stats
            avg_stats = {}
            for stat in base_stats:
                avg_stats[stat] = base_stats[stat] + (growths[stat] / 100.0) * levels_gained
            
            # Apply unpromoted stat caps (20 for most stats, 30 for Luck)
            for stat in avg_stats:
                if stat == 'Luck':
                    avg_stats[stat] = min(avg_stats[stat], 30)
                else:
                    avg_stats[stat] = min(avg_stats[stat], 20)
            
            return {
                'stats': avg_stats,
                'description': f"Level {target_level}",
                'class_name': row['Class']
            }
        
        elif len(level_parts) == 2:
            # Two-tier case: level1/level2
            tier0_level = int(level_parts[0])
            tier1_level = int(level_parts[1])
            
            # Calculate levels gained in base class
            tier0_levels = tier0_level - base_level
            if tier0_levels < 0:
                return None
            
            # Calculate levels gained in tier 1 class (starts at level 1)
            tier1_levels = tier1_level - 1
            if tier1_levels < 0:
                return None
            
            # Calculate stats after tier 0 levels
            stats_after_tier0 = {}
            for stat in base_stats:
                stats_after_tier0[stat] = base_stats[stat] + (growths[stat] / 100.0) * tier0_levels
            
            # Apply unpromoted stat caps before promotion
            for stat in stats_after_tier0:
                if stat == 'Luck':
                    stats_after_tier0[stat] = min(stats_after_tier0[stat], 30)
                elif stat == 'HP':
                    stats_after_tier0[stat] = min(stats_after_tier0[stat], 60)
                else:
                    stats_after_tier0[stat] = min(stats_after_tier0[stat], 20)
            
            # Get tier 1 promotion gains
            tier1_gains = {
                'HP': int(row['HP Gains']) if row['HP Gains'] else 0,
                'Pow': int(row['Pow Gains']) if row['Pow Gains'] else 0,
                'Skl': int(row['Skl Gains']) if row['Skl Gains'] else 0,
                'Spd': int(row['Spd Gains']) if row['Spd Gains'] else 0,
                'Def': int(row['Def Gains']) if row['Def Gains'] else 0,
                'Res': int(row['Res Gains']) if row['Res Gains'] else 0,
                'Luck': 0  # Luck typically doesn't get promotion gains
            }
            
            # Apply tier 1 gains
            for stat in stats_after_tier0:
                stats_after_tier0[stat] += tier1_gains[stat]
            
            # Calculate final stats after tier 1 levels
            avg_stats = {}
            for stat in stats_after_tier0:
                avg_stats[stat] = stats_after_tier0[stat] + (growths[stat] / 100.0) * tier1_levels
            
            # Apply tier 1 stat cap (20 for most stats, 30 for Luck - same as unpromoted)
            for stat in avg_stats:
                if stat == 'Luck':
                    avg_stats[stat] = min(avg_stats[stat], 30)
                elif stat == 'HP':
                    avg_stats[stat] = min(avg_stats[stat], 60)
                else:
                    avg_stats[stat] = min(avg_stats[stat], 20)
            
            promotion_class = row['Promotion Class'] if row['Promotion Class'] else "Promoted"
            
            return {
                'stats': avg_stats,
                'description': f"Level {tier0_level}/{tier1_level}",
                'class_name': promotion_class
            }
        
        else:  # len(level_parts) == 3
            # Three-tier case: level1/level2/level3
            tier0_level = int(level_parts[0])
            tier1_level = int(level_parts[1])
            tier2_level = int(level_parts[2])
            
            # Calculate levels gained in each tier
            tier0_levels = tier0_level - base_level
            if tier0_levels < 0:
                return None
            
            tier1_levels = tier1_level - 1
            if tier1_levels < 0:
                return None
            
            tier2_levels = tier2_level - 1
            if tier2_levels < 0:
                return None
            
            # Calculate stats after tier 0 levels
            stats_after_tier0 = {}
            for stat in base_stats:
                stats_after_tier0[stat] = base_stats[stat] + (growths[stat] / 100.0) * tier0_levels
            
            # Apply unpromoted stat caps before first promotion
            for stat in stats_after_tier0:
                if stat == 'Luck':
                    stats_after_tier0[stat] = min(stats_after_tier0[stat], 30)
                elif stat == 'HP':
                    avg_stats[stat] = min(avg_stats[stat], 60)
                else:
                    stats_after_tier0[stat] = min(stats_after_tier0[stat], 20)
            
            # Get tier 1 promotion gains
            tier1_gains = {
                'HP': int(row['HP Gains']) if row['HP Gains'] else 0,
                'Pow': int(row['Pow Gains']) if row['Pow Gains'] else 0,
                'Skl': int(row['Skl Gains']) if row['Skl Gains'] else 0,
                'Spd': int(row['Spd Gains']) if row['Spd Gains'] else 0,
                'Def': int(row['Def Gains']) if row['Def Gains'] else 0,
                'Res': int(row['Res Gains']) if row['Res Gains'] else 0,
                'Luck': 0
            }
            
            # Apply tier 1 gains
            for stat in stats_after_tier0:
                stats_after_tier0[stat] += tier1_gains[stat]
            
            # Calculate stats after tier 1 levels
            stats_after_tier1 = {}
            for stat in stats_after_tier0:
                stats_after_tier1[stat] = stats_after_tier0[stat] + (growths[stat] / 100.0) * tier1_levels
            
            # Apply tier 1 stat cap before second promotion (20 for most stats, 30 for Luck)
            for stat in stats_after_tier1:
                if stat == 'Luck':
                    stats_after_tier1[stat] = min(stats_after_tier1[stat], 30)
                elif stat == 'HP':
                    stats_after_tier1[stat] = min(stats_after_tier1[stat], 60)
                else:
                    stats_after_tier1[stat] = min(stats_after_tier1[stat], 20)
            
            # Get tier 2 promotion gains
            tier2_gains = {
                'HP': int(row['HP Gains 2']) if row['HP Gains 2'] else 0,
                'Pow': int(row['Pow Gains 2']) if row['Pow Gains 2'] else 0,
                'Skl': int(row['Skl Gains 2']) if row['Skl Gains 2'] else 0,
                'Spd': int(row['Spd Gains 2']) if row['Spd Gains 2'] else 0,
                'Def': int(row['Def Gains 2']) if row['Def Gains 2'] else 0,
                'Res': int(row['Res Gains 2']) if row['Res Gains 2'] else 0,
                'Luck': 0
            }
            
            # Apply tier 2 gains
            for stat in stats_after_tier1:
                stats_after_tier1[stat] += tier2_gains[stat]
            
            # Calculate final stats after tier 2 levels
            avg_stats = {}
            for stat in stats_after_tier1:
                avg_stats[stat] = stats_after_tier1[stat] + (growths[stat] / 100.0) * tier2_levels
            
            # Apply promoted stat cap (30 for all stats)
            for stat in avg_stats:
                if stat == 'HP':
                    avg_stats[stat] = min(avg_stats[stat], 60)
                avg_stats[stat] = min(avg_stats[stat], 30)
            
            tier2_class = row['Promotion Class 2'] if row['Promotion Class 2'] else "Promoted (Tier 2)"
            
            return {
                'stats': avg_stats,
                'description': f"Level {tier0_level}/{tier1_level}/{tier2_level}",
                'class_name': tier2_class
            }
    
    except (ValueError, KeyError):
        return None

def get_averaged_stats_embed(row, level_string):
    """
    Create an embed showing averaged stats for a unit at a given level.
    """
    result = calculate_average_stats(row, level_string)
    
    if result is None:
        return None
    
    stats = result['stats']
    
    # Create embed
    embed = discord.Embed(
        title=f"{row['Name']} {row['Affinity']} - {result['description']}", 
        color=0x4e3ca3
    )
    embed.set_thumbnail(url=row['Portrait'])
    embed.add_field(name="Class", value=result['class_name'], inline=True)
    
    # Format averaged stats (rounded to 1 decimal)
    avg_bases = (f"HP {stats['HP']:.1f} | "
                 f"Pow {stats['Pow']:.1f} | "
                 f"Skl {stats['Skl']:.1f} | "
                 f"Spd {stats['Spd']:.1f} | "
                 f"Lck {stats['Luck']:.1f} | "
                 f"Def {stats['Def']:.1f} | "
                 f"Res {stats['Res']:.1f}")
    
    embed.add_field(name="Average Stats", value=avg_bases, inline=False)
    
    return embed


#cota = cromar.create_subgroup("cota", "Get Call of the Armor data")

async def unit(ctx, name: str, levels: str = None):
    """
    Display unit data. Optionally calculate average stats at a given level.
    
    Usage:
        /unit [name] - Show base unit data
        /unit [name] [level] - Show average stats at level (e.g., /unit Puzon 10)
        /unit [name] [level]/[level] - Show average stats after first promotion (e.g., /unit Puzon 10/5)
        /unit [name] [level]/[level]/[level] - Show stats after second promotion (e.g., /unit Athos 10/10/5)
    """
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('auc/auc_unit.csv', newline='' , encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                was_found = True
                
                # If levels parameter is provided, show averaged stats
                if levels is not None:
                    embed = get_averaged_stats_embed(row, levels)
                    if embed is None:
                        await ctx.response.send_message(
                            "Invalid level format. Use format like `10`, `10/5`, or `10/10/5`."
                        )
                    else:
                        await ctx.response.send_message(embed=embed)
                else:
                    # Show standard unit data
                    paginator = pages.Paginator(
                        pages=get_unit_pages(row), 
                        show_menu=True, 
                        show_disabled=False, 
                        show_indicator=False, 
                        menu_placeholder="Select page to view", 
                        timeout=120, 
                        disable_on_timeout=True
                    )
                    await paginator.respond(ctx.interaction)
                break
        
        if not was_found:
            await ctx.response.send_message("That unit does not exist.")

async def item(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)            
    with open('auc/auc_item.csv', newline='') as csvfile:
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
                    if(row['Display Price'] == 'Yes'):
                        price = int(row['Uses']) * int(row['Price Per Use'])
                        price_string = str(price) + "G"
                        unitembed.add_field(name='Price: ', value=price_string, inline=False)
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
    if (row['Promotion Class'] == 'Rogue'):
        gains += " | "
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
    names = ["Iron Sword","Slim Sword","Steel Sword","Silver Sword","Iron Blade","Steel Blade","Silver Blade","Poison Sword","Gale Blade","Rapier","Noble Rapier","Dirk","Glaurung","Brave Sword","Regal Blade","Regale Blade","Killing Edge","Wo Dao","Goujian","Rune Blade","Mani Katti","Sol Katti","Binding Blade","Durandal","Armorslayer","Zanbato","Zanbato","Wyrmslayer","Magebane","Light Brand","Wind Sword","Flame Blade","Runesword","Lunar Blade","Lancereaver","Zweihander","Oni Katti","Deus Katti","Iron Lance","Slim Lance","Steel Lance","Silver Lance","Heartpiercer","Military Fork","Brave Lance","Killer Lance","Heavy Spear","Ridersbane","Ridersbane","Knightkneeler","Dragonpike","Duren's Spear","Feimazuo Dao","Javelin","Short Spear","Spear","Vaida's Spear","Rose of War","Nibelung","Axereaver","Reginleif","Saunion","Pilum","Iron Axe","The Iron Axe","Slim Axe","Steel Axe","Silver Axe","Battle Axe","Wolf Beil","Armads","Brave Axe","Raionos","Basilikos","Enduring Soul","Elimine Axe","Elimine Axe","Killer Axe","Halberd","Hammer","Dragon Axe","Devil Axe","Hand Axe","Short Axe","Tomahawk","Hatchet","Swordreaver","Swordslayer","Ax o' The Titan","Iron Bow","Short Bow","Steel Bow","Silver Bow","Poison Bow","Delphi","Skadi","Killer Bow","Brave Bow","Moonbow","Swiftshot","Spellseal Bow","Spellseal Bow","Longbow","Greatbow","Hwatcha","Ballista","Iron Ballista","Whale Hunter","Kraken Hunter","Fire","Thunder","Elfire","Bolting","Fimbulvter","Aircalibur","Cleanse","Shock Burst","Airblade","Forblaze","Lightning","Lightning","Shine","Divine","Thani","Purge","Aura","Morphic Dirge","Piety","Star Burst","Ivaldi","Flux","Luna","Malaise","Nosferatu","Eclipse","Fenrir","Ereshkigal","Shadow Shrike","Gespenst","Moon Burst","Munio","Heal","Mend","Recover","Poultice","Relaxing Melody","Physic","Darkmend","Fortify","Latona","Restore","Refreshing Herb","Silence","Sleep","Dissonant Chord","Rescue","Warp","Torch","Hammerne","Unlock","Barrier","Demon Light","Firestone","Icestone","Magestone","Earthstone","Dragonstone","Divinestone","Shadowstone","Firestone X","Wretched Air","Angelic Robe","Energy Ring","Secret Book","Speedwing","Goddess Icon","Dracoshield","Talisman","Body Ring","Boots","Metis's Tome","Member Card","Hoplon Guard","Fili Shield","Teal Gem","Red Gem","Blue Gem","Gold Gem","Chest Key","Chest Key (5)","Door Key","Master Key","Vulnerary","Vulnerary (60)","Elixir","Pure Water","Torch","Light Rune","Hero Crest","Knight Crest","Orion's Bolt","Elysian Whip","Guiding Ring","Ocean Seal","Heaven Seal","Master Seal","Caller Seal","Filla's Might","Sake","Eduardo's Ring","Jewel of Fire","Jewel of Fire","Ancient Scale","Fire Emblem"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
