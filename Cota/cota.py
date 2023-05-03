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


#cota = cromar.create_subgroup("cota", "Get Call of the Armor data")

async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('Cota/cota unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                paginator = pages.Paginator(pages=get_unit_pages(row), show_menu=True, show_disabled=False, show_indicator=False, menu_placeholder="Select page to view", timeout =120, disable_on_timeout = True)
                await paginator.respond(ctx.interaction)
                was_found = True
                break
        if (not was_found):
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
    return [name for name in names if name.lower().startswith(ctx.value.lower())]