import discord
import csv
import urllib
from discord.ext import pages

url_base = "https://raw.githubusercontent.com/laqieer/FEHR/master/"

affinity_icons = {
    'None': '',
    'Fire': '<:AffinFire:1083548172254720080>',
    'Thunder': '<:AffinThunder:1083548174637084703>',
    'Wind': '<:AffinWind:1083548175928926208>',
    'Water': '<:AffinIce:1083548173190045817>',
    'Dark': '<:AffinDark:1083548169901707285>',
    'Light': '<:AffinLight:1083548171281641583>',
    'Anima': '<:AffinAnima:1083548168672792697>',
}

face_names = {
    'Avatar': 'Hood',
    'Veronica': 'Veronica_Normal',
    'Bruno': 'Bruno_Masked',
}

def calc(expr):
    return str(int(eval(expr)))

def fmt(text):
    return text.strip().replace('TCC_NEWLINE', '').replace('""', '\n').replace('\\"', '""').replace('\\', '').replace('", "', '","')

def get_unit_data():
    unit_data = ['nameTextId,descriptionTextId,id,job,portrait,miniPortrait,affinity,sortID,Lv,baseHp,baseStr,baseSkl,baseSpd,baseDef,baseRes,baseLuk,baseConBonus,levelSword,levelLance,levelAxe,levelBow,levelStaff,levelAnima,levelLight,levelDark,growthHp,growthStr,growthSkl,growthSpd,growthDef,growthRes,growthLuk,paletteIdUnpromoted,paletteIdPromoted,battleAnimationIdUnpromoted,battleAnimationIdPromoted,pad_27,ability_mountedAid,ability_moveAgain,ability_steal,ability_theifKey,ability_dance,ability_play,ability_criticalBonus,ability_ballista,ability_promoted,ability_supplyDepot,ability_mountedIcon,ability_dragonKnightIcon,ability_pegasusKnightIcon,ability_lord,ability_female,ability_boss,ability_RoyWeaponLock,ability_WoDaoWeaponLock,ability_dragonStoneWeaponLock,ability_morph,ability_preventControl,ability_pegasusTriangleAttack,ability_armorTriangleAttack,ability_forbidden,ability_noExp,ability_lethality,ability_magicSeal,ability_dropLastItem,ability_EliwoodWeaponLock,ability_HectorWeaponLock,ability_LynWeaponLock,ability_AthosWeaponLock,support,dialogueId,comment']
    lines = [l.decode('utf-8') for l in urllib.request.urlopen(url_base + 'src/character.c').readlines()]
    for line in lines:
        if ' -> ' in line and '//{' not in line and 'Generic' not in line and 'Enemy' not in line:
            unit_data.append(line)
    return unit_data

def get_skill_data():
    skill_data = ['Type,NameJ,DescriptionJ,Name,Description']
    lines = [l.decode('shift-jis') for l in urllib.request.urlopen(url_base + 'src/skill.c').readlines()]
    start = lines.index('const struct SpecialSkill specialSkills[] = {\n') + 2
    end = lines.index('const u16 itemSpecialSkills[0x100] = {\n') - 2
    for i in range(start, end, 13):
        skill_data.append('<:SkillSpecial:1147751958770352209>,' + ''.join([fmt(x) for x in lines[i+1:i+5]]))
    start = lines.index('const struct AssistSkill assistSkills[] = {\n') + 2
    end = lines.index('char *getAssistSkillNameTextInActionMenu()\n') - 2
    for i in range(start, end):
        skill_data.append('<:SkillAssist:1147751954387324990>,' + fmt(lines[i])[1:-2])
    start = lines.index('const struct PassiveSkill passiveSkillAs[] = {\n') + 2
    end = lines.index('const u16 characterPassiveSkillAs[0x100][4] = {\n') - 2
    for i in range(start, end):
        skill_data.append('<:SkillPassiveA:1147751949563863120>,' + fmt(lines[i])[1:-2])
    start = lines.index('const struct PassiveSkill passiveSkillBs[] = {\n') + 2
    end = lines.index('const u16 characterPassiveSkillBs[0x100][4] = {\n') - 2
    for i in range(start, end):
        skill_data.append('<:SkillPassiveB:1147751945050783805>,' + fmt(lines[i])[1:-2])
    start = lines.index('const struct PassiveSkill passiveSkillCs[] = {\n') + 2
    end = lines.index('const u16 characterPassiveSkillCs[0x100][4] = {\n') - 2
    for i in range(start, end):
        skill_data.append('<:SkillPassiveC:1147751947282161734>,' + fmt(lines[i])[1:-2])
    start = lines.index('const struct PassiveSkill passiveSkillSs[] = {\n') + 2
    end = lines.index('const u16 itemPassiveSkillSs[0x100] = {\n') - 2
    for i in range(start, end):
        skill_data.append('<:SkillSacredSeal:1147751941015883797>,' + fmt(lines[i])[1:-2])
    return skill_data

def get_unit_pages(row):
    unitname=row['comment'].split(' -> ')[1]
    unitembed=discord.Embed(title=unitname + " " + affinity_icons[row['affinity'].strip()], color=0xD4BB77)
    unitembed.set_thumbnail(url=url_base + 'res/gfx/portrait/portrait_' + face_names.get(unitname, unitname) + '.png')
    unitembed.add_field(name="Lv" + row['Lv'] + " ", value=' '.join(word.title() for word in row['job'][len(' JOB_ID_'):].split('_')), inline=True)
    bases = "HP " + calc(row['baseHp']) + " | " + "Atk " + calc(row['baseStr']) + " | Skl " + calc(row['baseSkl']) + " | " + "Spd " + calc(row['baseSpd']) + " | " + "Lck " + calc(row['baseLuk']) + " | " + "Def " + calc(row['baseDef']) + " | " + "Res " + calc(row['baseRes'])
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + calc(row['growthHp']) + "% | " + "Atk " + calc(row['growthStr']) + "% | Skl " + calc(row['growthSkl']) + "% | " + "Spd " + calc(row['growthSpd']) + "% | " + "Lck " + calc(row['growthLuk']) + "% | " + "Def " + calc(row['growthDef']) + "% | " + "Res " + calc(row['growthRes']) + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = fehr_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)

    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        )
    ]
    return page_groups

async def unit(ctx, name: str):
    reader = csv.DictReader(get_unit_data())
    was_found = False
    for row in reader:
        if(row['comment'].strip().lower().endswith(' -> ' + name.strip().lower())):
            paginator = pages.Paginator(pages=get_unit_pages(row), show_menu=True, show_disabled=False, show_indicator=False, menu_placeholder="Select page to view", timeout =120, disable_on_timeout = True)
            await paginator.respond(ctx.interaction)
            was_found = True
            break
    if (not was_found):
        await ctx.response.send_message("That unit does not exist.")

async def skill(ctx, name: str):
    reader = csv.DictReader(get_skill_data())
    was_found = False
    for row in reader:
        if(row['Name'].strip().lower() == name.strip().lower()):
            skillembed=discord.Embed(title=row['Name'] + " " + row['Type'] + "\n" + row['NameJ'], color=0xac6c6c)
            skillembed.add_field(name='Description: ', value=row['Description'] + "\n" + row['DescriptionJ'], inline=False)
            was_found = True
            await ctx.response.send_message(embed=skillembed)
            break
    if (not was_found):
        await ctx.response.send_message("That skill does not exist.")


def fehr_get_ranks(row):
    ranks = ""
    if (row['levelSword'][-1] != '0'):
        ranks += "<:RankSword:1083549037585768510>Sword: " + row['levelSword'][len(' WPN_EXP_'):] + " | "
    if (row['levelLance'][-1] != '0'):
        ranks += "<:RankLance:1083549035622846474>Lance: " + row['levelLance'][len(' WPN_EXP_'):] + " | "
    if (row['levelAxe'][-1] != '0'):
        ranks += "<:RankAxe:1083549032292548659>Axe: " + row['levelAxe'][len(' WPN_EXP_'):] + " | "
    if (row['levelBow'][-1] != '0'):
        ranks += "<:RankBow:1083549033429205073>Bow: " + row['levelBow'][len(' WPN_EXP_'):] + " | "
    if (row['levelStaff'][-1] != '0'):
        ranks += "<:RankStaff:1083549038936326155>Staff: " + row['levelStaff'][len(' WPN_EXP_'):] + " | "
    if (row['levelAnima'][-1] != '0'):
        ranks += "<:RankAnima:1083549030598049884>Anima: " + row['levelAnima'][len(' WPN_EXP_'):] + " | "
    if (row['levelLight'][-1] != '0'):
        ranks += "<:RankLight:1083549037019541614>Light: " + row['levelLight'][len(' WPN_EXP_'):] + " | "
    if (row['levelDark'][-1] != '0'):
        ranks += "<:RankDark:1083549034310012959>Dark: " + row['levelDark'][len(' WPN_EXP_'):] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "None"
    return ranks

def get_unit_names(ctx):
    names = ['Alfons', 'Anna', 'Sharon', 'Laevatain', 'Hood', 'Laegjarn', 'Lif', 'Helbindi', 'Hell', 'Gustaf', 'Veronica', 'Bruno', 'Freya', 'Fjorm', 'Elm', 'Cerise', 'Srasir', 'Yurg', 'Freeze', 'Reghin', 'Ash', 'Loki', 'Fafnir', 'Eir', 'Scabiosa', 'Plumeria', 'Dagr', 'Nott', 'Froda', 'Takumi', 'Fafnir2', 'Peony', 'Avatar', 'Surtr', 'Eitri', 'Mirabilis', 'Otr', 'Marks']
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

def get_skill_names(ctx):
    names = ['Surefooted', 'Seior Shell', 'Guard Bearing 2', 'Earthwater Balm', "Loki's Temptation 2", 'Flow Refresh 2', 'Steady Stance 2', 'Miracle', 'Blazing Thunder', 'Steady Stance 1', 'Flower of Plenty 4', 'Rally Resistance', 'Guard 3', "Time's Pulse 2", 'Glimmer', "Surtr's Menace", 'Swift Sparrow 3', 'Fire Emblem 4', 'Fortress Res 3', 'Distant Counter', 'Speed 4', 'Def/Res Gap 4', 'Threaten Spd 4', 'Atk Smoke 3', 'Threaten Def 1', 'Aether', 'Sparkling Boost', 'New Moon', 'Flower of Joy 2', 'Flower of Sorrow 2', 'Sorcery Blade 2', 'Lull Atk/Def 4', 'Rally Def/Res+', 'Chill Atk 4', 'Guard Bearing 4', 'Threat. Atk/Def 3', 'Harsh Command+', 'Rally Spd/Res+', 'Spur Res 1', 'Atk Smoke 2', 'Quickened Pulse', 'Atk/Def Catch 4', 'Iceberg', 'Wary Fighter 2', 'Rally Up Atk', 'Ice Mirror', 'Shield Pulse 3', 'Aegis', 'Threat. Atk/Spd 1', 'Spur Atk 4', "Time's Pulse 4", 'Odd Atk Wave 1', 'Hardy Bearing', 'Flower of Ease 2', 'Deadly Balance', 'Fortify Res 4', 'Spd Tactic 4', 'Whimsical Dream', 'Panic Smoke 2', 'Chilling Wind', 'Gray Waves', 'Blazing Light', 'Spur Res 3', 'Pivot', 'Blazing Princess 2', 'Wary Fighter 4', 'Res Ploy 4', 'Rally Atk/Spd+', 'Earthwater Balm+', "Loki's Temptation 1", 'Def/Res Gap 2', 'Ardent Sacrifice', 'Fire Emblem 1', 'Panic Smoke 1', 'Frightful Dream', 'Fortress Res 4', 'Atk Smoke 4', 'Sabotage Spd 3', 'Spur Atk 3', 'Twin Blades', 'Earthfire Balm', 'Atk/Def Catch 2', 'Mystic Boost 2', 'Blazing Wind', 'Queen of Nightmare 4', 'Lofnheior 3', 'Savage Blow 2', 'Aerobatics 4', 'Odd Spd Wave 4', 'Fortify Res 1', 'Atk/Spd Push 1', 'Lull Spd/Def 3', 'Renewal 2', 'Spd Tactic 3', 'Spd Tactic 2', 'Flower of Sorrow 1', 'Chill Spd 3', 'A/D Near Trace 2', 'Threaten Spd 3', 'Panic Smoke 4', 'Flow Refresh 1', 'Death Blow 1', 'Sun-Twin Wing', 'Distant Guard 3', 'Heavy Blade 2', 'Lull Atk/Def 2', 'Rally Atk/Res', 'Atk/Spd Solo 4', 'Mystic Boost 3', 'Fortify Def 1', 'Aerobatics 2', 'Dragon Fang', 'Retribution', 'Death Blow 4', 'Gentle Dream', 'Flower of Ease 4', 'Pulse Smoke 2', 'Atk/Res Solo 2', 'Regnal Astra', 'Atk/Def Link 4', 'Queen of Nightmare 1', 'Guard Bearing 3', "Loki's Temptation 4", 'Inevitable Death', 'Heavy Blade 4', 'Def/Res Gap 1', 'Freezing Seal', 'Blazing Princess 3', 'Atk/Spd Solo 1', 'Radiant Aether', 'Death Blow 2', 'Guard Bearing 1', 'Aerobatics 1', 'Fortress Res 1', 'Wary Fighter 3', 'Sol', 'Renewal 1', 'Rally Up Res', 'Solid-Earth Balm', 'Binding Necklace', 'Sorcery Blade 3', 'Sabotage Def 4', 'Killing Intent', 'Shove', "Loki's Temptation 3", 'Odd Atk Wave 4', 'Fortify Res 3', 'Atk/Def Bond 1', 'Supply', 'Sabotage Def 1', 'Panic Smoke 3', 'Pulse Smoke 3', 'Heavenly Light', "Hel's Reaper", 'Spur Res 2', 'Vantage 4', 'Speed 2', 'Windfire Balm', 'Spd/Res Rein 2', 'Rally Up Atk+', 'Threaten Def 2', 'Nioavellir Axiom', 'Rally Up Res+', 'Growing Flame', 'Queen of Nightmare 3', 'Lull Atk/Def 3', 'Rally Def/Res', 'Res Ploy 1', 'Atk/Res Solo 3', 'Fireflood Balm+', 'Muspellflame', 'Sabotage Def 2', 'Savage Blow 1', 'Chill Atk 1', 'Fortify Def 2', 'Atk/Spd Push 3', 'Drive Atk 1', 'Lull Spd/Def 2', 'Shield Pulse 2', 'Blazing Princess 1', 'Steady Stance 4', 'Deflect Melee', 'Distant Guard 2', 'Fireflood Balm', 'Infantry Pulse 2', 'Glacies', 'Heavy Blade 3', 'Luck 1', 'Sabotage Spd 4', 'Death Blow 3', 'Threaten Spd 1', 'Sirius', 'Fire Emblem 2', 'Vantage 2', 'Windfire Balm+', 'Mystic Boost 4', 'Threat. Atk/Spd 3', 'Threaten Def 3', 'Wary Fighter 1', 'Pulse Smoke 1', 'Even Tempest 4', 'Atk/Spd Push 2', 'Future Vision', 'Black Luna', 'Swift Sparrow 1', 'Spd/Res Rein 4', 'Drive Atk 2', 'Atk/Res Rein 1', 'Flow Refresh 3', "Time's Pulse 3", 'Swift-Winds Balm', 'Luck 4', 'Vantage 1', 'Savage Blow 3', 'Atk/Spd Menace', 'Atk/Def Bond 3', 'Flower of Ease 3', 'Atk/Spd Solo 3', 'Odd Spd Wave 2', 'Luna', 'Distant Guard 1', 'Blazing Flame', 'Even Tempest 3', 'Flow Refresh 4', 'Close Counter', 'Rally Attack', 'Mystic Boost 1', 'Rally Defense', 'Odd Spd Wave 1', 'Renewal 3', 'Even Tempest 2', 'Opening Retainer', 'Drive Atk 3', 'Noontime', 'A/D Near Trace 1', 'Moonbow', 'Lunar Flash', 'Res Ploy 3', 'Lofnheior 2', 'Chill Atk 2', 'Res Ploy 2', 'Ignis', 'Threat. Atk/Spd 2', 'Lofnheior 1', 'Still-Water Balm', 'Atk Smoke 1', 'Luck 3', 'Darting Blow 4', 'Rally Atk/Def+', 'Pulse Smoke 4', 'Earthfire Balm+', 'Spur Atk 1', 'Flower of Sorrow 3', 'Pavise', 'Glowing Ember', 'Shield Pulse 4', 'Fire Emblem 3', 'Darting Blow 2', 'Sorcery Blade 1', 'Chill Spd 4', 'Luck 2', 'Atk/Def Catch 3', 'Atk/Def Link 2', 'Moon-Twin Wing', 'Deflect Magic', 'Atk/Def Menace', 'Sacrifice', 'Rally Speed', 'Reposition', 'Sweet Dreams', 'Speed 3', 'Flower of Ease 1', 'Vengeance', 'Swap', 'Def/Res Gap 3', 'Flower of Sorrow 4', 'Flashing Blade 1', 'Reciprocal Aid', 'Atk/Res Rein 3', 'Chill Spd 1', 'Daylight', 'Threaten Spd 2', 'Flower of Plenty 2', 'Swift Sparrow 2', 'Fire Emblem', 'Atk/Def Bond 4', 'Flower of Plenty 3', 'Queen of Nightmare 2', 'Flower of Joy 1', 'Draconic Aura', 'Fortify Def 3', 'A/D Near Trace 4', 'Atk/Spd Push 4', 'Fury 4', 'Atk/Def Link 1', 'Infantry Pulse 4', 'Sabotage Spd 1', 'Darting Blow 3', 'Chill Spd 2', 'Rising Thunder', 'Odd Atk Wave 3', 'Growing Light', 'Rising Flame', 'Dragon Gaze', 'Spd/Res Rein 1', 'Draw Back', 'To Change Fate!', 'Reprisal', 'Rising Wind', 'Flower of Plenty 1', 'Sabotage Spd 2', 'Fortify Res 2', 'Spd Tactic 1', 'Buckler', 'Fortress Res 2', 'Ruptured Sky', "Embla's Ward", "Njorun's Zeal", 'Infinite Nightmare', 'Shield Pulse 1', 'Heavy Blade 1', 'Sorcery Blade 4', 'Fury 3', 'Divine Recreation', 'Renewal 4', 'Smite', 'Chill Atk 3', 'Flower of Joy 4', 'Guard 2', 'Atk/Res Solo 4', 'Spur Atk 2', 'Rally Spd/Def+', 'Bonfire', 'Infantry Pulse 3', 'Atk/Spd Solo 2', 'Harsh Command', 'Savage Blow 4', 'Vantage 3', 'Imbue', 'Kindled-Fire Balm', 'Threat. Atk/Def 2', 'Sacred Cowl', 'Sabotage Def 3', 'Rally Atk/Spd', 'Distant Guard 4', 'Atk/Def Catch 1', 'Speed 1', 'Darting Blow 1', 'Holy Vestments', 'Fury 2', 'Rally Spd/Res', "Time's Pulse 1", 'Threaten Def 4', 'Threat. Atk/Def 1', 'Brutal Shell', 'Night Sky', 'Chilling Seal', 'Steady Stance 3', 'Rally Atk/Res+', 'Flashing Blade 2', 'Flashing Blade 4', 'Rally Spd/Def', 'Guard 1', 'Spd/Res Rein 3', 'Infantry Pulse 1', 'Even Tempest 1', 'Galeforce', 'A/D Near Trace 3', 'Flower of Joy 3', "Grani's Shield", 'Flashing Blade 3', 'Atk/Def Bond 2', 'Growing Wind', 'Atk/Res Rein 2', 'Lull Spd/Def 4', 'Spur Res 4', 'Deflect Missile', 'Blue Flame', 'Escutcheon', 'Growing Thunder', 'Astra', 'Fury 1', 'Lull Spd/Def 1', 'Lull Atk/Def 1', 'Atk/Res Solo 1', 'Odd Atk Wave 2', 'Lofnheior 4', 'Rising Light', 'Fortify Def 4', 'Rally Atk/Def', 'Aerobatics 3', 'Imperial Astra', 'Blazing Princess 4', 'Odd Spd Wave 3', 'Atk/Def Unity', 'Guard 4', 'Atk/Def Link 3', 'Armored Boots', 'Atk/Res Rein 4']
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]

if __name__ == '__main__':
    reader = csv.DictReader(get_skill_data())
    skills = set()
    for row in reader:
        skills.add(row['Name'])
    print(skills)
