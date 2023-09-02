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
    csvfile = url_base + 'doc/bot/fehr%20unit.csv'
    with urllib.request.urlopen(csvfile) as f:
        lines = [l.decode('utf-8') for l in f.readlines()]
        reader = csv.DictReader(lines)
        was_found = False
        for row in reader:
            if(row['comment'].strip().lower().endswith(' -> ' + name.strip().lower())):
                paginator = pages.Paginator(pages=get_unit_pages(row), show_menu=True, show_disabled=False, show_indicator=False, menu_placeholder="Select page to view", timeout =120, disable_on_timeout = True)
                await paginator.respond(ctx.interaction)
                was_found = True
                break
        if (not was_found):
            await ctx.response.send_message("That unit does not exist.")


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
    names = ['Alfons', 'Anna', 'Sharon', 'Laevatain', 'Hood', 'Laegjarn', 'Lif', 'Helbindi', 'Hell', 'Gustaf', 'Veronica', 'Bruno', 'Freya', 'Fjorm', 'Elm', 'Cerise', 'Srasir', 'Yurg', 'Otr', 'Freeze', 'Reghin', 'Ash', 'Loki', 'Fafnir', 'Eir', 'Scabiosa', 'Plumeria', 'Dagr', 'Nott', 'Froda', 'Takumi', 'Fafnir2', 'Peony', 'Avatar', 'Surtr', 'Eitri', 'Mirabilis', 'Otr', 'Hell']
    names.sort()
    return [name for name in names if name.lower().startswith(ctx.value.lower())]
