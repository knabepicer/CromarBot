import discord
import csv
import re
import random
from discord.ext import pages

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0xD4BB77)
    unitembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    #unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Atk " + row['Atk'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Atk " + row['Atk Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = ee_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotes'] == "Yes"):
        gains = ee_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)

    promoembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0xD4BB77)
    promoembed.set_thumbnail(url=row['Portrait'])
    promofound = False
    with open('ee/ee extra promos.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for promorow in reader:
            if(row['Name'] == promorow['Name']):
                promoembed.add_field(name="From " + promorow['Base Class 1'] + " to " + promorow['Promo Class 1'], value=ee_get_extra_gains(promorow, "1"), inline=True)
                promoembed.add_field(name="From " + promorow['Base Class 2'] + " to " + promorow['Promo Class 2'], value=ee_get_extra_gains(promorow, "2"), inline=True)
                promofound = True
                break

    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        )
    ]
    if (promofound):
        page_groups.append(pages.PageGroup
        (
        pages=[promoembed],
        label="Second Tier Promotions",
        description="Data on second tier promotions for trainee unit",
        use_default_buttons=False,
        )
        )
    return page_groups

def calculate_average_stats(row, level_string, tier1_class=None, tier2_class=None):
    """
    Calculate average stats for a unit at given level(s).
    Applies stat caps: 20 for tier 0/1 (30 for Luck, 60 for HP), 30 for tier 2 (60 for HP).
    
    Supports up to 3 tiers for trainee units (Gruyere, Jenna).
    
    Args:
        row: CSV row containing unit data
        level_string: String in format "10", "10/5", or "10/10/5"
        tier1_class: Optional tier 1 class name
        tier2_class: Optional tier 2 class name
    
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
            'Atk': int(row['Atk']),
            'Skl': int(row['Skl']),
            'Spd': int(row['Spd']),
            'Luck': int(row['Luck']),
            'Def': int(row['Def']),
            'Res': int(row['Res'])
        }
        
        # Get growth rates (as percentages)
        growths = {
            'HP': int(row['HP Growth']),
            'Atk': int(row['Atk Growth']),
            'Skl': int(row['Skl Growth']),
            'Spd': int(row['Spd Growth']),
            'Luck': int(row['Luck Growth']),
            'Def': int(row['Def Growth']),
            'Res': int(row['Res Growth'])
        }
        
        # Check if this is a trainee unit (Gruyere or Jenna)
        is_trainee = row['Name'] in ['Gruyere', 'Jenna']
        
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
            # For trainees (Gruyere, Jenna): tier 0 → tier 1 (both cap at 20)
            # For everyone else: tier 1 → tier 2 (tier 2 caps at 30)
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
            
            # Determine which tier 1 promotion to use
            use_promotion_2 = False
            selected_class = row['Promotion Class']
            
            if tier1_class:
                # Check if the specified class matches either promotion option
                stripped_input = re.sub(r'[^a-zA-Z0-9]', '', tier1_class).lower()
                
                promo_class_1 = re.sub(r'[^a-zA-Z0-9]', '', row['Promotion Class']).lower()
                promo_class_2 = re.sub(r'[^a-zA-Z0-9]', '', row['Promotion Class 2']).lower() if row['Promotion Class 2'] else ''
                
                if promo_class_2 and stripped_input == promo_class_2:
                    use_promotion_2 = True
                    selected_class = row['Promotion Class 2']
            
            # Get tier 1 promotion gains
            if use_promotion_2:
                tier1_gains = {
                    'HP': int(row['HP Gains 2']) if row['HP Gains 2'] else 0,
                    'Atk': int(row['Atk Gains 2']) if row['Atk Gains 2'] else 0,
                    'Skl': int(row['Skl Gains 2']) if row['Skl Gains 2'] else 0,
                    'Spd': int(row['Spd Gains 2']) if row['Spd Gains 2'] else 0,
                    'Def': int(row['Def Gains 2']) if row['Def Gains 2'] else 0,
                    'Res': int(row['Res Gains 2']) if row['Res Gains 2'] else 0,
                    'Luck': 0
                }
            else:
                tier1_gains = {
                    'HP': int(row['HP Gains']) if row['HP Gains'] else 0,
                    'Atk': int(row['Atk Gains']) if row['Atk Gains'] else 0,
                    'Skl': int(row['Skl Gains']) if row['Skl Gains'] else 0,
                    'Spd': int(row['Spd Gains']) if row['Spd Gains'] else 0,
                    'Def': int(row['Def Gains']) if row['Def Gains'] else 0,
                    'Res': int(row['Res Gains']) if row['Res Gains'] else 0,
                    'Luck': 0
                }
            
            # Apply tier 1 gains
            for stat in stats_after_tier0:
                stats_after_tier0[stat] += tier1_gains[stat]
            
            # Calculate final stats after tier 1 levels
            avg_stats = {}
            for stat in stats_after_tier0:
                avg_stats[stat] = stats_after_tier0[stat] + (growths[stat] / 100.0) * tier1_levels
            
            if is_trainee:
                # Trainees: tier 0 → tier 1, still caps at 20 (30 for Luck, 60 for HP)
                for stat in avg_stats:
                    if stat == 'Luck':
                        avg_stats[stat] = min(avg_stats[stat], 30)
                    elif stat == 'HP':
                        avg_stats[stat] = min(avg_stats[stat], 60)
                    else:
                        avg_stats[stat] = min(avg_stats[stat], 20)
            else:
                # Everyone else: tier 1 → tier 2, caps at 30 (60 for HP)
                for stat in avg_stats:
                    if stat == 'HP':
                        avg_stats[stat] = min(avg_stats[stat], 60)
                    else:
                        avg_stats[stat] = min(avg_stats[stat], 30)
            
            return {
                'stats': avg_stats,
                'description': f"Level {tier0_level}/{tier1_level}",
                'class_name': selected_class
            }
        
        else:  # len(level_parts) == 3
            # Three-tier case: level1/level2/level3 (only for trainees)
            if not is_trainee:
                return None  # Non-trainees can't have 3 tiers
            
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
            
            # Determine which tier 1 promotion to use
            use_tier1_promo_2 = False
            selected_tier1_class = row['Promotion Class']
            
            if tier1_class:
                stripped_input = re.sub(r'[^a-zA-Z0-9]', '', tier1_class).lower()
                promo_class_1 = re.sub(r'[^a-zA-Z0-9]', '', row['Promotion Class']).lower()
                promo_class_2 = re.sub(r'[^a-zA-Z0-9]', '', row['Promotion Class 2']).lower() if row['Promotion Class 2'] else ''
                
                if promo_class_2 and stripped_input == promo_class_2:
                    use_tier1_promo_2 = True
                    selected_tier1_class = row['Promotion Class 2']
            
            # Get tier 1 promotion gains
            if use_tier1_promo_2:
                tier1_gains = {
                    'HP': int(row['HP Gains 2']) if row['HP Gains 2'] else 0,
                    'Atk': int(row['Atk Gains 2']) if row['Atk Gains 2'] else 0,
                    'Skl': int(row['Skl Gains 2']) if row['Skl Gains 2'] else 0,
                    'Spd': int(row['Spd Gains 2']) if row['Spd Gains 2'] else 0,
                    'Def': int(row['Def Gains 2']) if row['Def Gains 2'] else 0,
                    'Res': int(row['Res Gains 2']) if row['Res Gains 2'] else 0,
                    'Luck': 0
                }
            else:
                tier1_gains = {
                    'HP': int(row['HP Gains']) if row['HP Gains'] else 0,
                    'Atk': int(row['Atk Gains']) if row['Atk Gains'] else 0,
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
            
            # Apply tier 1 stat cap before second promotion (20 for most stats, 30 for Luck, 60 for HP)
            for stat in stats_after_tier1:
                if stat == 'Luck':
                    stats_after_tier1[stat] = min(stats_after_tier1[stat], 30)
                elif stat == 'HP':
                    stats_after_tier1[stat] = min(stats_after_tier1[stat], 60)
                else:
                    stats_after_tier1[stat] = min(stats_after_tier1[stat], 20)
            
            # Now find tier 2 promotion gains from extra promos CSV
            tier2_gains = {'HP': 0, 'Atk': 0, 'Skl': 0, 'Spd': 0, 'Def': 0, 'Res': 0, 'Luck': 0}
            selected_tier2_class = "Promoted (Tier 2)"
            
            # Determine which tier 1 class was used to find the right tier 2 path
            base_class_for_tier2 = selected_tier1_class
            
            # Look up tier 2 promotions
            with open('ee/ee extra promos.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for promo_row in reader:
                    if promo_row['Name'] == row['Name']:
                        # Try to match tier 2 class if specified
                        if tier2_class:
                            stripped_input = re.sub(r'[^a-zA-Z0-9]', '', tier2_class).lower()
                            
                            # Check both promo class options
                            for i in [1, 2]:
                                promo_class_col = f'Promo Class {i}'
                                if promo_row[promo_class_col]:
                                    stripped_promo = re.sub(r'[^a-zA-Z0-9]', '', promo_row[promo_class_col]).lower()
                                    if stripped_input == stripped_promo:
                                        selected_tier2_class = promo_row[promo_class_col]
                                        tier2_gains = {
                                            'HP': int(promo_row[f'HP Gains {i}']) if promo_row[f'HP Gains {i}'] else 0,
                                            'Atk': int(promo_row[f'Atk Gains {i}']) if promo_row[f'Atk Gains {i}'] else 0,
                                            'Skl': int(promo_row[f'Skl Gains {i}']) if promo_row[f'Skl Gains {i}'] else 0,
                                            'Spd': int(promo_row[f'Spd Gains {i}']) if promo_row[f'Spd Gains {i}'] else 0,
                                            'Def': int(promo_row[f'Def Gains {i}']) if promo_row[f'Def Gains {i}'] else 0,
                                            'Res': int(promo_row[f'Res Gains {i}']) if promo_row[f'Res Gains {i}'] else 0,
                                            'Luck': 0
                                        }
                                        break
                        else:
                            # No tier 2 class specified - default based on tier 1 class
                            # Match Base Class to determine which path
                            for i in [1, 2]:
                                base_class_col = f'Base Class {i}'
                                if promo_row[base_class_col]:
                                    stripped_base = re.sub(r'[^a-zA-Z0-9]', '', promo_row[base_class_col]).lower()
                                    stripped_tier1 = re.sub(r'[^a-zA-Z0-9]', '', base_class_for_tier2).lower()
                                    if stripped_base == stripped_tier1:
                                        selected_tier2_class = promo_row[f'Promo Class {i}']
                                        tier2_gains = {
                                            'HP': int(promo_row[f'HP Gains {i}']) if promo_row[f'HP Gains {i}'] else 0,
                                            'Atk': int(promo_row[f'Atk Gains {i}']) if promo_row[f'Atk Gains {i}'] else 0,
                                            'Skl': int(promo_row[f'Skl Gains {i}']) if promo_row[f'Skl Gains {i}'] else 0,
                                            'Spd': int(promo_row[f'Spd Gains {i}']) if promo_row[f'Spd Gains {i}'] else 0,
                                            'Def': int(promo_row[f'Def Gains {i}']) if promo_row[f'Def Gains {i}'] else 0,
                                            'Res': int(promo_row[f'Res Gains {i}']) if promo_row[f'Res Gains {i}'] else 0,
                                            'Luck': 0
                                        }
                                        break
                        break
            
            # Apply tier 2 gains
            for stat in stats_after_tier1:
                stats_after_tier1[stat] += tier2_gains[stat]
            
            # Calculate final stats after tier 2 levels
            avg_stats = {}
            for stat in stats_after_tier1:
                avg_stats[stat] = stats_after_tier1[stat] + (growths[stat] / 100.0) * tier2_levels
            
            # Apply tier 2 stat cap (30 for all stats except HP at 60)
            for stat in avg_stats:
                if stat == 'HP':
                    avg_stats[stat] = min(avg_stats[stat], 60)
                else:
                    avg_stats[stat] = min(avg_stats[stat], 30)
            
            return {
                'stats': avg_stats,
                'description': f"Level {tier0_level}/{tier1_level}/{tier2_level}",
                'class_name': selected_tier2_class,
                'tier1_class': selected_tier1_class
            }
    
    except (ValueError, KeyError):
        return None

def get_averaged_stats_embed(row, level_string, tier1_class=None, tier2_class=None):
    """
    Create an embed showing averaged stats for a unit at a given level.
    """
    result = calculate_average_stats(row, level_string, tier1_class, tier2_class)
    
    if result is None:
        return None
    
    stats = result['stats']
    
    # Create embed
    embed = discord.Embed(
        title=f"{row['Name']} {row['Affinity']} - {result['description']}", 
        color=0xD4BB77
    )
    embed.set_thumbnail(url=row['Portrait'])
    embed.add_field(name="Class", value=result['class_name'], inline=True)
    
    # Format averaged stats (rounded to 1 decimal)
    avg_bases = (f"HP {stats['HP']:.1f} | "
                 f"Atk {stats['Atk']:.1f} | "
                 f"Skl {stats['Skl']:.1f} | "
                 f"Spd {stats['Spd']:.1f} | "
                 f"Lck {stats['Luck']:.1f} | "
                 f"Def {stats['Def']:.1f} | "
                 f"Res {stats['Res']:.1f}")
    
    embed.add_field(name="Average Stats", value=avg_bases, inline=False)
    
    return embed


#ee = cromar.create_subgroup("ee", "Get Embers Entwined data")

async def unit(ctx, name: str, levels: str = None, tier1_class: str = None, tier2_class: str = None):
    """
    Display unit data. Optionally calculate average stats at a given level.
    
    Usage:
        /unit [name] - Show base unit data
        /unit [name] [level] - Show average stats at level (e.g., /unit Petra 10)
        /unit [name] [level]/[level] - Show average stats after promotion (e.g., /unit Petra 10/5)
        /unit [name] [level]/[level] [class] - Show stats with specific tier 1 class
        /unit [name] [level]/[level]/[level] [tier1] [tier2] - For trainees (e.g., /unit Gruyere 10/10/5 AxeMercenary Hero)
    """
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('ee/ee unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                was_found = True
                
                # If levels parameter is provided, show averaged stats
                if levels is not None:
                    embed = get_averaged_stats_embed(row, levels, tier1_class, tier2_class)
                    if embed is None:
                        await ctx.response.send_message(
                            "Invalid level format. Use format like `10`, `10/5`, or `10/10/5` (for trainees)."
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


def ee_get_ranks(row):
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

def ee_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != '0'):
        gains += "HP: +" + row['HP Gains'] + " | "
    if (row['Atk Gains'] != '0'):
        gains += "Atk: +" + row['Atk Gains'] + " | "
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
            gains3 += "HP: +" + row['HP Gains 2'] + " | "
        if (row['Atk Gains 2'] != '0'):
            gains3 += "Atk: +" + row['Atk Gains 2'] + " | "
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

def ee_get_extra_gains(row, num):
    gains = ""
    if (row['HP Gains ' + num] != '0'):
        gains += "HP: +" + row['HP Gains ' + num] + " | "
    if (row['Atk Gains ' + num] != '0'):
        gains += "Atk: +" + row['Atk Gains ' + num] + " | "
    if (row['Skl Gains ' + num] != '0'):
        gains += "Skl: +" + row['Skl Gains ' + num] + " | "
    if (row['Spd Gains ' + num] != '0'):
        gains += "Spd: +" + row['Spd Gains ' + num] + " | "
    if (row['Def Gains ' + num] != '0'):
        gains += "Def: +" + row['Def Gains ' + num] + " | "
    if (row['Res Gains ' + num] != '0'):
        gains += "Res: +" + row['Res Gains ' + num] + " | "
    if (row['Con Gains ' + num] != '0'):
        gains += "Con: +" + row['Con Gains ' + num] + " | "
    if (row['Mov Gains ' + num] != '0'):
            gains += "Mov: " + row['Mov Gains ' + num] + " | "
    gains = gains[:-3]
    gains += "\n"
    if (row['Sword Gains ' + num] != 'None'):
        gains += "<:RankSword:1083549037585768510>" + row['Sword Gains ' + num] + " | "
    if (row['Lance Gains ' + num] != 'None'):
        gains += "<:RankLance:1083549035622846474>" + row['Lance Gains ' + num] + " | "
    if (row['Axe Gains ' + num] != 'None'):
        gains += "<:RankAxe:1083549032292548659>" + row['Axe Gains ' + num] + " | "
    if (row['Bow Gains ' + num] != 'None'):
        gains += "<:RankBow:1083549033429205073>" + row['Bow Gains ' + num] + " | "
    if (row['Staff Gains ' + num] != 'None'):
        gains += "<:RankStaff:1083549038936326155>" + row['Staff Gains ' + num] + " | "
    if (row['Anima Gains ' + num] != 'None'):
        gains += "<:RankAnima:1083549030598049884>" + row['Anima Gains ' + num] + " | "
    if (row['Light Gains ' + num] != 'None'):
        gains += "<:RankLight:1083549037019541614>" + row['Light Gains ' + num] + " | "
    if (row['Dark Gains ' + num] != 'None'):
        gains += "<:RankDark:1083549034310012959>" + row['Dark Gains ' + num] + " | "
    gains = gains[:-3]

    return gains

def get_unit_names(ctx):
    names = ["Petra", "Rasmus", "Liam", "Leif", "Deesa", "Diego", "Terry", "Erina", "Rumina", "Grunhilde", "DeAndre", "Amaran", "Swyftpawe", "Zaid", "Chayse", "Kane", "Turner", "Datura", "Wisteria", "Pavani", "Randolf", "Mary", "Torie", "Tillie", "Jeff", "Alvaro", "Ben", "Enoch", "Iris", "Masato", "Hanson", "Chell", "Gruyere", "Hemming", "Miuu", "Baal", "Phileas", "Ryland", "Serah", "Jason", "Jenna", "Eustace", "Christel", "Garland", "Coltrane", "Georgio", "S", "Flavius"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
