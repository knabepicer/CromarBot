import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0xb6bfb8)
    #supportembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x34c290)
    unitembed.set_thumbnail(url=row['Portrait'])
    #supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] + " | " + "Mag " + row['Mag'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Mov']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | " + "Mag " + row['Mag Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = hag_get_ranks(row)
    unitembed.add_field(name="Skills", value=row['Skills'], inline=False)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotion Class'] != ""):
        gains = hag_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    
    
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

def calculate_average_stats(row, level_string, promotion_class=None):
    """
    Calculate average stats for a unit at given level(s).
    
    Args:
        row: CSV row containing unit data
        level_string: String in format "10" or "10/5"
        promotion_class: Optional string specifying which promotion class to use
    
    Returns:
        Dictionary with calculated stats, or None if invalid input
    """
    # Parse the level string
    level_parts = level_string.split('/')
    
    if len(level_parts) > 2:
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
        
        # Calculate total levels gained
        if len(level_parts) == 1:
            # Simple case: just one level value
            target_level = int(level_parts[0])
            levels_gained = target_level - base_level
            
            if levels_gained < 0:
                return None  # Can't go below base level
            
            # Calculate average stats
            avg_stats = {}
            for stat in base_stats:
                avg_stats[stat] = base_stats[stat] + (growths[stat] / 100.0) * levels_gained
            
            return {
                'stats': avg_stats,
                'levels_gained': levels_gained,
                'description': f"Level {target_level}",
                'class_name': row['Class']
            }
        
        else:
            # Promoted case: level1/level2
            unpromoted_level = int(level_parts[0])
            promoted_level = int(level_parts[1])
            
            # Calculate levels gained in base class
            unpromoted_levels = unpromoted_level - base_level
            if unpromoted_levels < 0:
                return None
            
            # Calculate levels gained in promoted class (promoted class starts at level 1)
            promoted_levels = promoted_level - 1
            if promoted_levels < 0:
                return None
            
            total_levels = unpromoted_levels + promoted_levels
            
            # Calculate stats after unpromoted levels
            stats_at_promotion = {}
            for stat in base_stats:
                stats_at_promotion[stat] = base_stats[stat] + (growths[stat] / 100.0) * unpromoted_levels
            
            # Determine which promotion path to use
            use_promotion_2 = False
            selected_class = row['Promotion Class']
            
            if promotion_class:
                # Check if the specified class matches either promotion option
                stripped_input = re.sub(r'[^a-zA-Z0-9]', '', promotion_class).lower()
                
                promo_class_1 = re.sub(r'[^a-zA-Z0-9]', '', row['Promotion Class']).lower()
                promo_class_2 = re.sub(r'[^a-zA-Z0-9]', '', row['Promotion Class 2']).lower() if row['Promotion Class 2'] else ''
                
                if promo_class_2 and stripped_input == promo_class_2:
                    use_promotion_2 = True
                    selected_class = row['Promotion Class 2']
                # If it matches promotion 1 or doesn't match either, use promotion 1 (default)
            
            # Add promotion gains based on selected promotion path
            if use_promotion_2:
                promotion_gains = {
                    'HP': int(row['HP Gains 2']) if row['HP Gains 2'] else 0,
                    'Str': int(row['Str Gains 2']) if row['Str Gains 2'] else 0,
                    'Mag': int(row['Mag Gains 2']) if row['Mag Gains 2'] else 0,
                    'Skl': int(row['Skl Gains 2']) if row['Skl Gains 2'] else 0,
                    'Spd': int(row['Spd Gains 2']) if row['Spd Gains 2'] else 0,
                    'Def': int(row['Def Gains 2']) if row['Def Gains 2'] else 0,
                    'Res': int(row['Res Gains 2']) if row['Res Gains 2'] else 0,
                    'Luck': 0  # Luck typically doesn't get promotion gains
                }
            else:
                promotion_gains = {
                    'HP': int(row['HP Gains']) if row['HP Gains'] else 0,
                    'Str': int(row['Str Gains']) if row['Str Gains'] else 0,
                    'Mag': int(row['Mag Gains']) if row['Mag Gains'] else 0,
                    'Skl': int(row['Skl Gains']) if row['Skl Gains'] else 0,
                    'Spd': int(row['Spd Gains']) if row['Spd Gains'] else 0,
                    'Def': int(row['Def Gains']) if row['Def Gains'] else 0,
                    'Res': int(row['Res Gains']) if row['Res Gains'] else 0,
                    'Luck': 0  # Luck typically doesn't get promotion gains
                }
            
            # Apply promotion gains
            for stat in stats_at_promotion:
                stats_at_promotion[stat] += promotion_gains[stat]
            
            # Calculate final stats after promoted levels
            avg_stats = {}
            for stat in stats_at_promotion:
                avg_stats[stat] = stats_at_promotion[stat] + (growths[stat] / 100.0) * promoted_levels
            
            final_class = selected_class if selected_class else "Promoted"
            
            return {
                'stats': avg_stats,
                'levels_gained': total_levels,
                'description': f"Level {unpromoted_level}/{promoted_level}",
                'class_name': final_class,
                'unpromoted_levels': unpromoted_levels,
                'promoted_levels': promoted_levels
            }
    
    except (ValueError, KeyError):
        return None

def get_averaged_stats_embed(row, level_string, promotion_class=None):
    """
    Create an embed showing averaged stats for a unit at a given level.
    """
    result = calculate_average_stats(row, level_string, promotion_class)
    
    if result is None:
        return None
    
    stats = result['stats']
    
    # Create embed
    embed = discord.Embed(
        title=f"{row['Name']} {row['Affinity']} - {result['description']}", 
        color=0xb6bfb8
    )
    embed.set_thumbnail(url=row['Portrait'])
    embed.add_field(name="Class", value=result['class_name'], inline=True)
    #embed.add_field(name="Total Levels Gained", value=str(result['levels_gained']), inline=True)
    
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
    
    # Show growths for reference
    """
    growths = (f"HP {row['HP Growth']}% | "
               f"Str {row['Str Growth']}% | "
               f"Mag {row['Mag Growth']}% | "
               f"Skl {row['Skl Growth']}% | "
               f"Spd {row['Spd Growth']}% | "
               f"Lck {row['Luck Growth']}% | "
               f"Def {row['Def Growth']}% | "
               f"Res {row['Res Growth']}%")
    embed.add_field(name="Growths", value=growths, inline=False)
    
    
    if 'unpromoted_levels' in result:
        details = f"Unpromoted levels: {result['unpromoted_levels']} | Promoted levels: {result['promoted_levels']}"
        embed.add_field(name="Level Breakdown", value=details, inline=False)
    """
    
    return embed

async def unit(ctx, name: str, levels: str = None):
    """
    Display unit data. Optionally calculate average stats at a given level.
    
    Usage:
        /unit [name] - Show base unit data
        /unit [name] [level] - Show average stats at level (e.g., /unit Kyra 10)
        /unit [name] [level]/[level] - Show average stats after promotion (e.g., /unit Kyra 10/5)
        /unit [name] [level]/[level] [class] - Show stats with specific promotion (e.g., /unit Agari 10/1 White Dragoon)
    """
    # Parse the input to separate levels from promotion class
    promotion_class = None
    level_string = levels
    
    if levels is not None:
        # Split by spaces to check if there's a class name
        parts = levels.split(None, 1)  # Split on first whitespace only
        if len(parts) > 1:
            level_string = parts[0]
            promotion_class = parts[1]
        else:
            level_string = parts[0]
    
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('hag/hag_unit.csv', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                was_found = True
                
                # If levels parameter is provided, show averaged stats
                if levels is not None:
                    embed = get_averaged_stats_embed(row, level_string, promotion_class)
                    if embed is None:
                        await ctx.response.send_message(
                            "Invalid level format. Use format like `10` or `10/5` (optionally followed by promotion class name)."
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

async def skill(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('hag/hag_skill.csv', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                unitembed=discord.Embed(title=row['Name'], color=0xb6bfb8)
                unitembed.add_field(name='Description: ', value=row['Description'], inline=False)
                was_found = True
                await ctx.response.send_message(embed=unitembed)
                break
        if (not was_found):
                await ctx.response.send_message("That skill does not exist.") 



def hag_get_ranks(row):
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

def hag_get_gains(row):
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
    #gains2 += '\n'
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
    names = ["Kyra","Apate","Phobos","Soter","Hecate","Kairos","Raleigh","Begoña","Fango","López","Edward","Agari","Pericles","Nikolaos","Jane","Hestia","Eupraxia","Tiresias","Wulfric","Pluto","Ofelia","Polonius","Alonso","Teresa","Delilah","Zaccheus","Simeon","Beatrix","Barlowe","Fiadh","Conan","Dahl","Nicaea","Telemus","Plato","Fazang","Jingyi","Xinyi","Ziying","Demeter","Jason","Laertes","Pheme","Vasiliki","Scymerius","Fructuoso","Mopsus","Coronis","Glaucus","Lorenzo","Thyone","Órlaith","Sandraudiga","Aura","Cybele","Dolus V", "Nestor", "Marina", "Alastor", "Dolus", "Elias", "Antiope", "Eudoxus", "Hippalus"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

def get_skill_names(ctx):
    names = ["Story Boon","Canto","Canto+","Outdoorswoman","Certain Blow","Renewal","Powerstaff","Crit Boost","Aptitude","Trauma","Reposition","Savior","Triangle Adept","Thunderstorm","Opportunist","Locktouch","Assassinate","Poison Strike","Reckless","Bow Range +1","Tome Range +1","Bow Breaker","Tomebreaker","Nullify","Daunt","Inspiration","Rally Spectrum","Rally Movement","Despoil","Stink","Perfume","Paragon","Discipline","Miracle","Method Acting","Bargain","Peacebringer","Forager","Shade","Provoke","Clumsy","Gamble","Frenzy","White Pool","Resolve","Intimidate","Savage Blow","Staff Savant","Void Curse","Blood Bounty","Supply"] 
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
