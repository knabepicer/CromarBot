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

def calculate_average_stats(row, level_string):
    """
    Calculate average stats for a unit at given level(s).
    Applies individual stat caps from the character's Cap columns.
    
    Stat caps:
    - Tier 0 (unpromoted): 20 for most stats, 30 for Luck, 60 for HP
    - Tier 1 (first promotion): 20 for most stats, 30 for Luck, 60 for HP
    - Tier 2 (second promotion): Uses individual caps from Str Cap, Mag Cap, etc.
    
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
            'Str': int(row['Str']),
            'Mag': int(row['Mag']),
            'Skl': int(row['Skl']),
            'Spd': int(row['Spd']),
            'Luck': int(row['Luck']),
            'Def': int(row['Def']),
            'Res': int(row['Res'])
        }
        
        # Get growth rates (as percentages)
        growths = {
            'HP': int(row['HP Growth']),
            'Str': int(row['Str Growth']),
            'Mag': int(row['Mag Growth']),
            'Skl': int(row['Skl Growth']),
            'Spd': int(row['Spd Growth']),
            'Luck': int(row['Luck Growth']),
            'Def': int(row['Def Growth']),
            'Res': int(row['Res Growth'])
        }
        
        # Get tier 2 caps from individual cap columns
        tier2_caps = {
            'HP': 60,  # Default HP cap
            'Str': int(row['Str Cap']) if row['Str Cap'] else 30,
            'Mag': int(row['Mag Cap']) if row['Mag Cap'] else 30,
            'Skl': int(row['Skl Cap']) if row['Skl Cap'] else 30,
            'Spd': int(row['Spd Cap']) if row['Spd Cap'] else 30,
            'Luck': 30,  # Default Luck cap
            'Def': int(row['Def Cap']) if row['Def Cap'] else 30,
            'Res': int(row['Res Cap']) if row['Res Cap'] else 30
        }
        
        # Calculate based on number of level segments
        if len(level_parts) == 1:
            # Simple case: just one level value (unpromoted or base tier)
            target_level = int(level_parts[0])
            levels_gained = target_level - base_level
            
            if levels_gained < 0:
                return None  # Can't go below base level
            
            # Calculate average stats
            avg_stats = {}
            for stat in base_stats:
                avg_stats[stat] = base_stats[stat] + (growths[stat] / 100.0) * levels_gained
            
            # Apply tier 0/1 stat caps (20 for most stats, 30 for Luck, 60 for HP)
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
            
            # Apply tier 0 stat caps before promotion
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
                'Str': int(row['Str Gains']) if row['Str Gains'] else 0,
                'Mag': int(row['Mag Gains']) if row['Mag Gains'] else 0,
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
            
            # Apply tier 1 stat caps (20 for most stats, 30 for Luck, 60 for HP)
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
            # Three-tier case: level1/level2/level3 (only Sally)
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
            
            # Apply tier 0 stat caps before first promotion
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
                'Str': int(row['Str Gains']) if row['Str Gains'] else 0,
                'Mag': int(row['Mag Gains']) if row['Mag Gains'] else 0,
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
            
            # Apply tier 1 stat caps before second promotion
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
                'Str': int(row['Str Gains 2']) if row['Str Gains 2'] else 0,
                'Mag': int(row['Mag Gains 2']) if row['Mag Gains 2'] else 0,
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
            
            # Apply tier 2 individual stat caps
            for stat in avg_stats:
                avg_stats[stat] = min(avg_stats[stat], tier2_caps[stat])
            
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
        color=0x0d59d4
    )
    embed.set_thumbnail(url=row['Portrait'])
    embed.add_field(name="Class", value=result['class_name'], inline=True)
    
    # Format averaged stats (rounded to 1 decimal)
    avg_bases = (f"HP {stats['HP']:.1f} | "
                 f"Str {stats['Str']:.1f} | "
                 f"Mag {stats['Mag']:.1f} | "
                 f"Skl {stats['Skl']:.1f} | "
                 f"Spd {stats['Spd']:.1f} | "
                 f"Lck {stats['Luck']:.1f} | "
                 f"Def {stats['Def']:.1f} | "
                 f"Res {stats['Res']:.1f}")
    
    embed.add_field(name="Average Stats", value=avg_bases, inline=False)
    
    return embed


async def unit(ctx, name: str, levels: str = None):
    """
    Display unit data. Optionally calculate average stats at a given level.
    
    Usage:
        /unit [name] - Show base unit data
        /unit [name] [level] - Show average stats at level (e.g., /unit Walter 10)
        /unit [name] [level]/[level] - Show average stats after first promotion (e.g., /unit Walter 10/5)
        /unit [name] [level]/[level]/[level] - Show stats after second promotion (e.g., /unit Sally 10/10/5)
    """
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('fourkings/four kings unit.csv', newline='') as csvfile:
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
