import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x2bc255)
    supportembed=discord.Embed(title=row['Name'] + " " + row['Affinity'], color=0x2bc255)
    if (row['Name'] == 'Eli' and random.randint(1, 10) > 7):
        unitembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081990677140869281/1115805496075632761/6Eli.png')
        supportembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081990677140869281/1115805496075632761/6Eli.png')
    elif (row['Name'] == 'Tactician' and random.randint(1, 10) > 5):
        unitembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081990677140869281/1115805495039635506/2Tactician2Female.png')
        supportembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081990677140869281/1115805495039635506/2Tactician2Female.png')
    elif (row['Name'] == 'Kiri' and random.randint(1, 10) > 5):
        unitembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081990677140869281/1115805633493610548/37Kiri2Wings.png')
        supportembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081990677140869281/1115805633493610548/37Kiri2Wings.png')
    elif (row['Name'] == 'Niya' and random.randint(1, 10) == 1):
        unitembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081990677140869281/1115805582851592202/24Niya2Possessed.png')
        supportembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081990677140869281/1115805582851592202/24Niya2Possessed.png')
    else:
        unitembed.set_thumbnail(url=row['Portrait'])
        supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    
    bases = "HP " + row['HP'] + " | " + "Atk " + row['Atk'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Atk " + row['Atk Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = dlatmol_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotion Class'] != ""):
        gains = dlatmol_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    
    with open('dlatmol/dlatmol_supports.csv', newline='') as csvfile:
        tact = False
        if (row['Name'] == 'Tactician'):
            tact = True
        reader = csv.DictReader(csvfile)
        for supportrow in reader:
            if (supportrow['Name'] == 'M!Tactician' and tact):
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
                supportembed.add_field(name="Male Supports", value=supportstring, inline=False)
            elif (supportrow['Name'] == 'F!Tactician' and tact):
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
                supportembed.add_field(name="Female Supports", value=supportstring, inline=False)
            elif (row['Name'] == supportrow['Name']):
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

 
    return page_groups

def calculate_average_stats(row, level_string):
    """
    Calculate average stats for a unit at given level(s).
    Applies stat caps: 20 unpromoted (30 for Luck), 30 promoted.
    
    Args:
        row: CSV row containing unit data
        level_string: String in format "10" or "10/5"
    
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
            
            # Calculate stats after unpromoted levels
            stats_at_promotion = {}
            for stat in base_stats:
                stats_at_promotion[stat] = base_stats[stat] + (growths[stat] / 100.0) * unpromoted_levels
            
            # Apply unpromoted stat caps before promotion
            for stat in stats_at_promotion:
                if stat == 'Luck':
                    stats_at_promotion[stat] = min(stats_at_promotion[stat], 30)
                elif stat == 'HP':
                    stats_at_promotion[stat] = min(stats_at_promotion[stat], 60)
                else:
                    stats_at_promotion[stat] = min(stats_at_promotion[stat], 20)
            
            # Add promotion gains
            promotion_gains = {
                'HP': int(row['HP Gains']) if row['HP Gains'] else 0,
                'Atk': int(row['Atk Gains']) if row['Atk Gains'] else 0,
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
            
            # Apply promoted stat cap (30 for all stats)
            for stat in avg_stats:
                if stat == 'HP':
                    avg_stats[stat] = min(avg_stats[stat], 60)
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
        color=0x2bc255
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
    


async def unit(ctx, name: str, levels: str = None):
    """
    Display unit data. Optionally calculate average stats at a given level.
    
    Usage:
        /unit [name] - Show base unit data
        /unit [name] [level] - Show average stats at level (e.g., /unit Orion 10)
        /unit [name] [level]/[level] - Show average stats after promotion (e.g., /unit Orion 10/5)
    """
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('dlatmol/dlatmol_unit.csv', newline='') as csvfile:
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
                            "Invalid level format. Use format like `10` or `10/5`."
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


def dlatmol_get_ranks(row):
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

def dlatmol_get_gains(row):
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
    return gains + gains2

def get_unit_names(ctx):
    names = ["Orion","Tactician","Francine","Shermie","Emma","Eli","Arthur","Blair","Hyle","Ronaldo","Aislin","Fiana","Horton","Yet","Dale","Chandra","Freesia","Sherie","Ashley","Wren","Raimon","Luca","James","Niya","Ty","Agrippa","Shanks","Mide","Alva","Darius","Suzhen","Dakini","Fang","Whitney","Vito","Egil","Kiri","Jenna","Kathe","Dorothy","Arjun","Khan","Adda","Ardoome","Durga","Maya"]
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
