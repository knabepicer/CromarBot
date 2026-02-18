import discord
import csv
import re
import random
from discord.ext import pages

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x47CAFF)
    supportembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x47CAFF)
    unitembed.set_thumbnail(url=row['Portrait'])
    supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    #unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Atk " + row['Atk'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Atk " + row['Atk Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = cota_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotes'] == "Yes"):
        gains = cota_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    
    with open('Cota/cota supports.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for supportrow in reader:
            if(row['Name'] == supportrow['Name']):
                supportstring = ""
                if(supportrow['Partner 1'] != '0'):
                    supportstring += supportrow['Partner 1'] + " : Base: " + supportrow['Starting Value 1'] + " | Growth: +" + supportrow['Growth 1'] + "\n"
                if(supportrow['Partner 2'] != '0'):
                    supportstring += supportrow['Partner 2'] + " : Base: " + supportrow['Starting Value 2'] + " | Growth: +" + supportrow['Growth 2'] + "\n"
                if(supportrow['Partner 3'] != '0'):
                    supportstring += supportrow['Partner 3'] + " : Base: " + supportrow['Starting Value 3'] + " | Growth: +" + supportrow['Growth 3'] + "\n"
                if(supportrow['Partner 4'] != '0'):
                    supportstring += supportrow['Partner 4'] + " : Base: " + supportrow['Starting Value 4'] + " | Growth: +" + supportrow['Growth 4'] + "\n"
                if(supportrow['Partner 5'] != '0'):
                    supportstring += supportrow['Partner 5'] + " : Base: " + supportrow['Starting Value 5'] + " | Growth: +" + supportrow['Growth 5'] + "\n"
                if(supportrow['Partner 6'] != '0'):
                    supportstring += supportrow['Partner 6'] + " : Base: " + supportrow['Starting Value 6'] + " | Growth: +" + supportrow['Growth 6'] + "\n"
                if(supportrow['Partner 7'] != '0'):
                    supportstring += supportrow['Partner 7'] + " : Base: " + supportrow['Starting Value 7'] + " | Growth: +" + supportrow['Growth 7'] + "\n"
                supportembed.add_field(name="", value=supportstring, inline=False)
    supportembed.set_footer(text="In Call of the Armor, supports are increased once at the start of a chapter if units are simultaneously deployed. 80 points are needed to reach C support, 160 for B, and 240 for A.")

    promoembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x47CAFF)
    promoembed.set_thumbnail(url=row['Portrait'])
    promofound = False
    with open('Cota/cota extra promos.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for promorow in reader:
            if(row['Name'] == promorow['Name']):
                promoembed.add_field(name="From " + promorow['Base Class 1'], value="", inline=True)
                promoembed.add_field(name=promorow['Promo Class 1'], value=cota_get_extra_gains(promorow, "1"), inline=True)
                promoembed.add_field(name=promorow['Promo Class 2'], value=cota_get_extra_gains(promorow, "2"), inline=True)
                promoembed.add_field(name="From " + promorow['Base Class 2'], value="", inline=True)
                promoembed.add_field(name=promorow['Promo Class 3'], value=cota_get_extra_gains(promorow, "3"), inline=True)
                promoembed.add_field(name=promorow['Promo Class 4'], value=cota_get_extra_gains(promorow, "4"), inline=True)
                promoembed.add_field(name="From " + promorow['Base Class 3'], value="", inline=True)
                promoembed.add_field(name=promorow['Promo Class 5'], value=cota_get_extra_gains(promorow, "5"), inline=True)
                promoembed.add_field(name=promorow['Promo Class 6'], value=cota_get_extra_gains(promorow, "6"), inline=True)
                promofound = True
                break

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
    Calculate average stats for a unit at given levels with optional promotion classes.
    
    Args:
        row: CSV row containing unit data from cota_unit.csv
        level_string: String in format "10", "10/5", or "10/10/5"
        tier1_class: Optional string specifying first promotion class (from cota_unit.csv)
        tier2_class: Optional string specifying second promotion class (from cota_extra_promos.csv)
    
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
                elif stat == 'HP':
                    avg_stats[stat] = min(avg_stats[stat], 60)
                else:
                    avg_stats[stat] = min(avg_stats[stat], 20)
            
            return {
                'stats': avg_stats,
                'description': f"Level {target_level}",
                'class_name': row['Class'],
                'tier': 0
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
            
            total_levels = tier0_levels + tier1_levels
            
            # Calculate stats after tier 0 levels
            stats_after_tier0 = {}
            for stat in base_stats:
                stats_after_tier0[stat] = base_stats[stat] + (growths[stat] / 100.0) * tier0_levels
            
            # Determine which tier 1 promotion to use
            tier1_promo_num = 1  # Default to Promotion Class
            selected_tier1_class = row['Promotion Class']
            
            if tier1_class:
                stripped_input = re.sub(r'[^a-zA-Z0-9]', '', tier1_class).lower()
                
                for i in range(1, 4):
                    promo_col = f'Promotion Class{" " + str(i) if i > 1 else ""}'
                    if row[promo_col]:
                        stripped_promo = re.sub(r'[^a-zA-Z0-9]', '', row[promo_col]).lower()
                        if stripped_input == stripped_promo:
                            tier1_promo_num = i
                            selected_tier1_class = row[promo_col]
                            break
            
            # Get tier 1 promotion gains
            suffix = "" if tier1_promo_num == 1 else f" {tier1_promo_num}"
            tier1_gains = {
                'HP': int(row[f'HP Gains{suffix}']) if row[f'HP Gains{suffix}'] else 0,
                'Atk': int(row[f'Atk Gains{suffix}']) if row[f'Atk Gains{suffix}'] else 0,
                'Skl': int(row[f'Skl Gains{suffix}']) if row[f'Skl Gains{suffix}'] else 0,
                'Spd': int(row[f'Spd Gains{suffix}']) if row[f'Spd Gains{suffix}'] else 0,
                'Def': int(row[f'Def Gains{suffix}']) if row[f'Def Gains{suffix}'] else 0,
                'Res': int(row[f'Res Gains{suffix}']) if row[f'Res Gains{suffix}'] else 0,
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
            
            return {
                'stats': avg_stats,
                'description': f"Level {tier0_level}/{tier1_level}",
                'class_name': selected_tier1_class,
                'tier': 1
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
            
            total_levels = tier0_levels + tier1_levels + tier2_levels
            
            # Calculate stats after tier 0 levels
            stats_after_tier0 = {}
            for stat in base_stats:
                stats_after_tier0[stat] = base_stats[stat] + (growths[stat] / 100.0) * tier0_levels
            
            # Apply unpromoted stat caps before first promotion
            for stat in stats_after_tier0:
                if stat == 'Luck':
                    stats_after_tier0[stat] = min(stats_after_tier0[stat], 30)
                elif stat == 'HP':
                    stats_after_tier0[stat] = min(stats_after_tier0[stat], 60)
                else:
                    stats_after_tier0[stat] = min(stats_after_tier0[stat], 20)
            
            # Determine which tier 1 promotion to use
            tier1_promo_num = 1  # Default to Promotion Class
            selected_tier1_class = row['Promotion Class']
            
            if tier1_class:
                stripped_input = re.sub(r'[^a-zA-Z0-9]', '', tier1_class).lower()
                
                for i in range(1, 4):
                    promo_col = f'Promotion Class{" " + str(i) if i > 1 else ""}'
                    if row[promo_col]:
                        stripped_promo = re.sub(r'[^a-zA-Z0-9]', '', row[promo_col]).lower()
                        if stripped_input == stripped_promo:
                            tier1_promo_num = i
                            selected_tier1_class = row[promo_col]
                            break
            
            # Get tier 1 promotion gains
            suffix = "" if tier1_promo_num == 1 else f" {tier1_promo_num}"
            tier1_gains = {
                'HP': int(row[f'HP Gains{suffix}']) if row[f'HP Gains{suffix}'] else 0,
                'Atk': int(row[f'Atk Gains{suffix}']) if row[f'Atk Gains{suffix}'] else 0,
                'Skl': int(row[f'Skl Gains{suffix}']) if row[f'Skl Gains{suffix}'] else 0,
                'Spd': int(row[f'Spd Gains{suffix}']) if row[f'Spd Gains{suffix}'] else 0,
                'Def': int(row[f'Def Gains{suffix}']) if row[f'Def Gains{suffix}'] else 0,
                'Res': int(row[f'Res Gains{suffix}']) if row[f'Res Gains{suffix}'] else 0,
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
            
            # Now find tier 2 promotion gains from extra promos CSV
            tier2_gains = {'HP': 0, 'Atk': 0, 'Skl': 0, 'Spd': 0, 'Def': 0, 'Res': 0, 'Luck': 0}
            selected_tier2_class = "Promoted (Tier 2)"
            
            # Look up tier 2 promotions
            with open('Cota/cota extra promos.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for promo_row in reader:
                    if promo_row['Name'] == row['Name']:
                        if tier2_class:
                            # User specified a tier 2 class - find the match
                            stripped_input = re.sub(r'[^a-zA-Z0-9]', '', tier2_class).lower()
                            
                            for i in range(1, 7):
                                promo_class_col = f'Promo Class {i}'
                                if promo_row[promo_class_col]:
                                    stripped_promo = re.sub(r'[^a-zA-Z0-9]', '', promo_row[promo_class_col]).lower()
                                    if stripped_input == stripped_promo:
                                        # Found the matching tier 2 class
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
                            # No tier 2 class specified - default to Promo Class 1
                            if promo_row['Promo Class 1']:
                                selected_tier2_class = promo_row['Promo Class 1']
                                tier2_gains = {
                                    'HP': int(promo_row['HP Gains 1']) if promo_row['HP Gains 1'] else 0,
                                    'Atk': int(promo_row['Atk Gains 1']) if promo_row['Atk Gains 1'] else 0,
                                    'Skl': int(promo_row['Skl Gains 1']) if promo_row['Skl Gains 1'] else 0,
                                    'Spd': int(promo_row['Spd Gains 1']) if promo_row['Spd Gains 1'] else 0,
                                    'Def': int(promo_row['Def Gains 1']) if promo_row['Def Gains 1'] else 0,
                                    'Res': int(promo_row['Res Gains 1']) if promo_row['Res Gains 1'] else 0,
                                    'Luck': 0
                                }
                        break
            
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
            
            return {
                'stats': avg_stats,
                'description': f"Level {tier0_level}/{tier1_level}/{tier2_level}",
                'class_name': selected_tier2_class,
                'tier1_class': selected_tier1_class,
                'tier': 2
            }
    
    except (ValueError, KeyError):
        return None

def get_averaged_stats_embed(row, level_string, tier1_class=None, tier2_class=None):
    """
    Create an embed showing averaged stats for a unit at given levels.
    """
    result = calculate_average_stats(row, level_string, tier1_class, tier2_class)
    
    if result is None:
        return None
    
    stats = result['stats']
    
    # Create embed
    embed = discord.Embed(
        title=f"{row['Name']} {row['Affinity']} - {result['description']}", 
        color=0x47CAFF
    )
    embed.set_thumbnail(url=row['Portrait'])
    
    if result['tier'] == 2:
        embed.add_field(name="Tier 1 Class", value=result['tier1_class'], inline=True)
        embed.add_field(name="Tier 2 Class", value=result['class_name'], inline=True)
    else:
        embed.add_field(name="Class", value=result['class_name'], inline=True)
    
    embed.add_field(name="Total Levels Gained", value=str(result['levels_gained']), inline=True)
    
    # Format averaged stats (rounded to 1 decimal)
    avg_bases = (f"HP {stats['HP']:.1f} | "
                 f"Atk {stats['Atk']:.1f} | "
                 f"Skl {stats['Skl']:.1f} | "
                 f"Spd {stats['Spd']:.1f} | "
                 f"Lck {stats['Luck']:.1f} | "
                 f"Def {stats['Def']:.1f} | "
                 f"Res {stats['Res']:.1f}")
    
    embed.add_field(name="Average Stats", value=avg_bases, inline=False)
    
    # Show growths for reference
    growths = (f"HP {row['HP Growth']}% | "
               f"Atk {row['Atk Growth']}% | "
               f"Skl {row['Skl Growth']}% | "
               f"Spd {row['Spd Growth']}% | "
               f"Lck {row['Luck Growth']}% | "
               f"Def {row['Def Growth']}% | "
               f"Res {row['Res Growth']}%")
    embed.add_field(name="Growths", value=growths, inline=False)
    
    if 'tier0_levels' in result:
        if result['tier'] == 2:
            details = f"Base levels: {result['tier0_levels']} | Tier 1 levels: {result['tier1_levels']} | Tier 2 levels: {result['tier2_levels']}"
        else:
            details = f"Base levels: {result['tier0_levels']} | Tier 1 levels: {result['tier1_levels']}"
        embed.add_field(name="Level Breakdown", value=details, inline=False)
    
    return embed

#cota = cromar.create_subgroup("cota", "Get Call of the Armor data")

async def unit(ctx, name: str, levels: str = None):
    """
    Display unit data. Optionally calculate average stats at given levels.
    
    Usage:
        /unit [name] - Show base unit data
        /unit [name] [level] - Show average stats at level (e.g., /unit Abdul 10)
        /unit [name] [level]/[level] [class] - Show stats with tier 1 promotion (e.g., /unit Abdul 10/5 Mage)
        /unit [name] [level]/[level]/[level] [class1] [class2] - Show stats with both promotions (e.g., /unit Abdul 10/10/5 Mage Sage)
    """
    # Parse the input to separate levels from promotion classes
    tier1_class = None
    tier2_class = None
    level_string = levels
    
    if levels is not None:
        # Split by spaces
        parts = levels.split()
        if len(parts) > 0:
            level_string = parts[0]
            if len(parts) > 1:
                tier1_class = parts[1]
            if len(parts) > 2:
                tier2_class = parts[2]
    
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('Cota/cota unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                was_found = True
                
                # If levels parameter is provided, show averaged stats
                if levels is not None:
                    embed = get_averaged_stats_embed(row, level_string, tier1_class, tier2_class)
                    if embed is None:
                        await ctx.response.send_message(
                            "Invalid level format. Use format like `10`, `10/5`, or `10/10/5` (optionally followed by class names)."
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


def cota_get_ranks(row):
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

def cota_get_gains(row):
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
        if (row['Atk Gains 2'] != '0'):
            gains += "Atk: +" + row['Atk Gains 2'] + " | "
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
    if (row['Promotes 3'] != 'No'): 
        gains += '\n' + row['Promotion Class 3'] + '\n'
        if (row['HP Gains 3'] != '0'):
            gains += "HP: +" + row['HP Gains 3'] + " | "
        if (row['Atk Gains 3'] != '0'):
            gains += "Atk: +" + row['Atk Gains 3'] + " | "
        if (row['Skl Gains 3'] != '0'):
            gains += "Skl: +" + row['Skl Gains 3'] + " | "
        if (row['Spd Gains 3'] != '0'):
            gains += "Spd: +" + row['Spd Gains 3'] + " | "
        if (row['Def Gains 3'] != '0'):
            gains += "Def: +" + row['Def Gains 3'] + " | "
        if (row['Res Gains 3'] != '0'):
            gains += "Res: +" + row['Res Gains 3'] + " | "
        if (row['Con Gains 3'] != '0'):
            gains += "Con: +" + row['Con Gains 3'] + " | "
        if (row['Mov Gains 3'] != '0'):
            if (int(row['Mov Gains 3']) > 0):
                gains += "Mov: +" + row['Mov Gains 3'] + " | "
            else:
                gains += "Mov: " + row['Mov Gains 3'] + " | "
        gains = gains[:-3]
        gains += "\n"
        if (row['Sword Gains 3'] != 'None'):
            if (row['Sword Gains 3'].isdigit()):
                gains += "<:RankSword:1083549037585768510>+" + row['Sword Gains 3'] + " | "
            else:
                gains += "<:RankSword:1083549037585768510>" + row['Sword Gains 3'] + " | "
        if (row['Lance Gains 3'] != 'None'):
            if (row['Lance Gains 3'].isdigit()):
                gains += "<:RankLance:1083549035622846474>+" + row['Lance Gains 3'] + " | "
            else:
                gains += "<:RankLance:1083549035622846474>" + row['Lance Gains 3'] + " | "
        if (row['Axe Gains 3'] != 'None'):
            if (row['Axe Gains 3'].isdigit()):
                gains += "<:RankAxe:1083549032292548659>+" + row['Axe Gains 3'] + " | "
            else:
                gains += "<:RankAxe:1083549032292548659>" + row['Axe Gains 3'] + " | "
        if (row['Bow Gains 3'] != 'None'):
            if (row['Bow Gains 3'].isdigit()):
                gains += "<:RankBow:1083549033429205073>+" + row['Bow Gains 3'] + " | "
            else:
                gains += "<:RankBow:1083549033429205073>" + row['Bow Gains 3'] + " | "
        if (row['Staff Gains 3'] != 'None'):
            if (row['Staff Gains 3'].isdigit()):
                gains += "<:RankStaff:1083549038936326155>+" + row['Staff Gains 3'] + " | "
            else:
                gains += "<:RankStaff:1083549038936326155>" + row['Staff Gains 3'] + " | "
        if (row['Anima Gains 3'] != 'None'):
            if (row['Anima Gains 3'].isdigit()):
                gains += "<:RankAnima:1083549030598049884>+" + row['Anima Gains 3'] + " | "
            else:
                gains += "<:RankAnima:1083549030598049884>" + row['Anima Gains 3'] + " | "
        if (row['Light Gains 3'] != 'None'):
            if (row['Light Gains 3'].isdigit()):
                gains += "<:RankLight:1083549037019541614>+" + row['Light Gains 3'] + " | "
            else:
                gains += "<:RankLight:1083549037019541614>" + row['Light Gains 3'] + " | "
        if (row['Dark Gains 3'] != 'None'):
            if (row['Dark Gains 3'].isdigit()):
                gains += "<:RankDark:1083549034310012959>+" + row['Dark Gains 3'] + " | "
            else:
                gains += "<:RankDark:1083549034310012959>" + row['Dark Gains 3'] + " | "
        gains = gains[:-3]
    return gains

def cota_get_extra_gains(row, num):
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
    names = ["Kuijia","Shale","Fernandez","Floor","Youngblood","Sjoerd","Noki","Daisy","Kilian","Philip","William","Ikechukwu","Sovnya","Mac","Hazel","Alair","Itoro","Drouin","D. Sunwing","Taika","Abdul","Lily","Vivek","Uyama","Ansha","Gu","Venus","Soma","Adine","Burdock","Josie","Frances","Poincare","Expirus","Maluj","Weber","Brioche","Bar'del","Seer","The Kamuth","Rienmire","Kalach","Millisent","Finwald","Alessia","Geirhart","Luan","Vectar","Giroux","Kim","Bloody Jeb","Arkell","Srikhandi","Flint","Queijo","Clothilde","Delano","Liam","Alderich","Strontium","Zain"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
