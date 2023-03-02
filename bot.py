import discord
import csv
import re
import random

def bob_get_ranks(row):
    ranks = ""
    if (row['Sword'] != 'NoRank'):
        ranks += "Sword: " + row['Sword'] + " | "
    if (row['Lance'] != 'NoRank'):
        ranks += "Lance: " + row['Lance'] + " | "
    if (row['Axe'] != 'NoRank'):
        ranks += "Axe: " + row['Axe'] + " | "
    if (row['Bow'] != 'NoRank'):
        ranks += "Bow: " + row['Bow'] + " | "
    if (row['Staff'] != 'NoRank'):
        ranks += "Staff: " + row['Staff'] + " | "
    if (row['Anima'] != 'NoRank'):
        ranks += "Anima: " + row['Anima'] + " | "
    if (row['Light'] != 'NoRank'):
        ranks += "Light: " + row['Light'] + " | "
    if (row['Dark'] != 'NoRank'):
        ranks += "Dark: " + row['Dark'] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "None"
    return ranks

def cota_get_ranks(row):
    ranks = ""
    if (row['Sword'] != 'None'):
        ranks += "Sword: " + row['Sword'] + " | "
    if (row['Lance'] != 'None'):
        ranks += "Lance: " + row['Lance'] + " | "
    if (row['Axe'] != 'None'):
        ranks += "Axe: " + row['Axe'] + " | "
    if (row['Bow'] != 'None'):
        ranks += "Bow: " + row['Bow'] + " | "
    if (row['Staff'] != 'None'):
        ranks += "Staff: " + row['Staff'] + " | "
    if (row['Anima'] != 'None'):
        ranks += "Anima: " + row['Anima'] + " | "
    if (row['Light'] != 'None'):
        ranks += "Light: " + row['Light'] + " | "
    if (row['Dark'] != 'None'):
        ranks += "Dark: " + row['Dark'] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "None"
    return ranks

def bob_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['Str Gains'] != 0):
        gains += "Str: +" + row['Str Gains'] + " | "
    if (row['Mag Gains'] != 0):
        gains += "Mag: +" + row['Mag Gains'] + " | "
    if (row['Skl Gains'] != 0):
        gains += "Skl: +" + row['Skl Gains'] + " | "
    if (row['Spd Gains'] != 0):
        gains += "Spd: +" + row['Spd Gains'] + " | "
    if (row['Def Gains'] != 0):
        gains += "Def: +" + row['Def Gains'] + " | "
    if (row['Res Gains'] != 0):
        gains += "Res: +" + row['Res Gains'] + " | "
    if (row['Bld Gains'] != 0):
        gains += "Bld: +" + row['Bld Gains'] + " | "
    if (row['Mov Gains'] != 0):
        gains += "Mov: +" + row['Mov Gains'] + " | "
    gains = gains[:-3]
    gains += "\n"
    if (row['Sword Gains'] != 'None'):
        if (row['Sword Gains'].isdigit()):
            gains += "Sword: +" + row['Sword Gains'] + " | "
        else:
            gains += "Sword: " + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
        if (row['Lance Gains'].isdigit()):
            gains += "Lance: +" + row['Lance Gains'] + " | "
        else:
            gains += "Lance: " + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
        if (row['Axe Gains'].isdigit()):
            gains += "Axe: +" + row['Axe Gains'] + " | "
        else:
            gains += "Axe: " + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
        if (row['Bow Gains'].isdigit()):
            gains += "Bow: +" + row['Bow Gains'] + " | "
        else:
            gains += "Bow: " + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
        if (row['Staff Gains'].isdigit()):
            gains += "Staff: +" + row['Staff Gains'] + " | "
        else:
            gains += "Staff: " + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
        if (row['Anima Gains'].isdigit()):
            gains += "Anima: +" + row['Anima Gains'] + " | "
        else:
            gains += "Anima: " + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
        if (row['Light Gains'].isdigit()):
            gains += "Light: +" + row['Light Gains'] + " | "
        else:
            gains += "Light: " + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
        if (row['Dark Gains'].isdigit()):
            gains += "Dark: +" + row['Dark Gains'] + " | "
        else:
            gains += "Dark: " + row['Dark Gains'] + " | "
    gains = gains[:-3]
    return gains

def cota_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != 0):
        gains += "HP: +" + row['HP Gains'] + " | "
    if (row['Atk Gains'] != 0):
        gains += "Atk: +" + row['Atk Gains'] + " | "
    if (row['Skl Gains'] != 0):
        gains += "Skl: +" + row['Skl Gains'] + " | "
    if (row['Spd Gains'] != 0):
        gains += "Spd: +" + row['Spd Gains'] + " | "
    if (row['Def Gains'] != 0):
        gains += "Def: +" + row['Def Gains'] + " | "
    if (row['Res Gains'] != 0):
        gains += "Res: +" + row['Res Gains'] + " | "
    if (row['Con Gains'] != 0):
        gains += "Con: +" + row['Con Gains'] + " | "
    if (row['Mov Gains'] != 0):
        gains += "Mov: +" + row['Mov Gains'] + " | "
    gains = gains[:-3]
    gains += "\n"
    if (row['Sword Gains'] != 'None'):
        if (row['Sword Gains'].isdigit()):
            gains += "Sword: +" + row['Sword Gains'] + " | "
        else:
            gains += "Sword: " + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
        if (row['Lance Gains'].isdigit()):
            gains += "Lance: +" + row['Lance Gains'] + " | "
        else:
            gains += "Lance: " + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
        if (row['Axe Gains'].isdigit()):
            gains += "Axe: +" + row['Axe Gains'] + " | "
        else:
            gains += "Axe: " + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
        if (row['Bow Gains'].isdigit()):
            gains += "Bow: +" + row['Bow Gains'] + " | "
        else:
            gains += "Bow: " + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
        if (row['Staff Gains'].isdigit()):
            gains += "Staff: +" + row['Staff Gains'] + " | "
        else:
            gains += "Staff: " + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
        if (row['Anima Gains'].isdigit()):
            gains += "Anima: +" + row['Anima Gains'] + " | "
        else:
            gains += "Anima: " + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
        if (row['Light Gains'].isdigit()):
            gains += "Light: +" + row['Light Gains'] + " | "
        else:
            gains += "Light: " + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
        if (row['Dark Gains'].isdigit()):
            gains += "Dark: +" + row['Dark Gains'] + " | "
        else:
            gains += "Dark: " + row['Dark Gains'] + " | "
    gains = gains[:-3]
    if (row['Promotes 2'] != 'No'): 
        gains += '\n' + row['Promotion Class 2'] + '\n'
        if (row['HP Gains 2'] != 0):
            gains += "HP: +" + row['HP Gains 2'] + " | "
        if (row['Atk Gains 2'] != 0):
            gains += "Atk: +" + row['Atk Gains 2'] + " | "
        if (row['Skl Gains 2'] != 0):
            gains += "Skl: +" + row['Skl Gains 2'] + " | "
        if (row['Spd Gains 2'] != 0):
            gains += "Spd: +" + row['Spd Gains 2'] + " | "
        if (row['Def Gains 2'] != 0):
            gains += "Def: +" + row['Def Gains 2'] + " | "
        if (row['Res Gains 2'] != 0):
            gains += "Res: +" + row['Res Gains 2'] + " | "
        if (row['Bld Gains 2'] != 0):
            gains += "Bld: +" + row['Bld Gains 2'] + " | "
        if (row['Mov Gains 2'] != 0):
            gains += "Mov: +" + row['Mov Gains 2'] + " | "
        gains = gains[:-3]
        gains += "\n"
        if (row['Sword Gains 2'] != 'None'):
            if (row['Sword Gains 2'].isdigit()):
                gains += "Sword: +" + row['Sword Gains 2'] + " | "
            else:
                gains += "Sword: " + row['Sword Gains 2'] + " | "
        if (row['Lance Gains 2'] != 'None'):
            if (row['Lance Gains 2'].isdigit()):
                gains += "Lance: +" + row['Lance Gains 2'] + " | "
            else:
                gains += "Lance: " + row['Lance Gains 2'] + " | "
        if (row['Axe Gains 2'] != 'None'):
            if (row['Axe Gains 2'].isdigit()):
                gains += "Axe: +" + row['Axe Gains 2'] + " | "
            else:
                gains += "Axe: " + row['Axe Gains 2'] + " | "
        if (row['Bow Gains 2'] != 'None'):
            if (row['Bow Gains 2'].isdigit()):
                gains += "Bow: +" + row['Bow Gains 2'] + " | "
            else:
                gains += "Bow: " + row['Bow Gains 2'] + " | "
        if (row['Staff Gains 2'] != 'None'):
            if (row['Staff Gains 2'].isdigit()):
                gains += "Staff: +" + row['Staff Gains 2'] + " | "
            else:
                gains += "Staff: " + row['Staff Gains 2'] + " | "
        if (row['Anima Gains 2'] != 'None'):
            if (row['Anima Gains 2'].isdigit()):
                gains += "Anima: +" + row['Anima Gains 2'] + " | "
            else:
                gains += "Anima: " + row['Anima Gains 2'] + " | "
        if (row['Light Gains 2'] != 'None'):
            if (row['Light Gains 2'].isdigit()):
                gains += "Light: +" + row['Light Gains 2'] + " | "
            else:
                gains += "Light: " + row['Light Gains 2'] + " | "
        if (row['Dark Gains 2'] != 'None'):
            if (row['Dark Gains 2'].isdigit()):
                gains += "Dark: +" + row['Dark Gains 2'] + " | "
            else:
                gains += "Dark: " + row['Dark Gains 2'] + " | "
        gains = gains[:-3]
    if (row['Promotes 3'] != 'No'): 
        gains += '\n' + row['Promotion Class 3'] + '\n'
        if (row['HP Gains 3'] != 0):
            gains += "HP: +" + row['HP Gains 3'] + " | "
        if (row['Atk Gains 3'] != 0):
            gains += "Atk: +" + row['Atk Gains 3'] + " | "
        if (row['Skl Gains 3'] != 0):
            gains += "Skl: +" + row['Skl Gains 3'] + " | "
        if (row['Spd Gains 3'] != 0):
            gains += "Spd: +" + row['Spd Gains 3'] + " | "
        if (row['Def Gains 3'] != 0):
            gains += "Def: +" + row['Def Gains 3'] + " | "
        if (row['Res Gains 3'] != 0):
            gains += "Res: +" + row['Res Gains 3'] + " | "
        if (row['Bld Gains 3'] != 0):
            gains += "Bld: +" + row['Bld Gains 3'] + " | "
        if (row['Mov Gains 3'] != 0):
            gains += "Mov: +" + row['Mov Gains 3'] + " | "
        gains = gains[:-3]
        gains += "\n"
        if (row['Sword Gains 3'] != 'None'):
            if (row['Sword Gains 3'].isdigit()):
                gains += "Sword: +" + row['Sword Gains 3'] + " | "
            else:
                gains += "Sword: " + row['Sword Gains 3'] + " | "
        if (row['Lance Gains 3'] != 'None'):
            if (row['Lance Gains 3'].isdigit()):
                gains += "Lance: +" + row['Lance Gains 3'] + " | "
            else:
                gains += "Lance: " + row['Lance Gains 3'] + " | "
        if (row['Axe Gains 3'] != 'None'):
            if (row['Axe Gains 3'].isdigit()):
                gains += "Axe: +" + row['Axe Gains 3'] + " | "
            else:
                gains += "Axe: " + row['Axe Gains 3'] + " | "
        if (row['Bow Gains 3'] != 'None'):
            if (row['Bow Gains 3'].isdigit()):
                gains += "Bow: +" + row['Bow Gains 3'] + " | "
            else:
                gains += "Bow: " + row['Bow Gains 3'] + " | "
        if (row['Staff Gains 3'] != 'None'):
            if (row['Staff Gains 3'].isdigit()):
                gains += "Staff: +" + row['Staff Gains 3'] + " | "
            else:
                gains += "Staff: " + row['Staff Gains 3'] + " | "
        if (row['Anima Gains 3'] != 'None'):
            if (row['Anima Gains 3'].isdigit()):
                gains += "Anima: +" + row['Anima Gains 3'] + " | "
            else:
                gains += "Anima: " + row['Anima Gains 3'] + " | "
        if (row['Light Gains 3'] != 'None'):
            if (row['Light Gains 3'].isdigit()):
                gains += "Light: +" + row['Light Gains 3'] + " | "
            else:
                gains += "Light: " + row['Light Gains 3'] + " | "
        if (row['Dark Gains 3'] != 'None'):
            if (row['Dark Gains 3'].isdigit()):
                gains += "Dark: +" + row['Dark Gains 3'] + " | "
            else:
                gains += "Dark: " + row['Dark Gains 3'] + " | "
        gains = gains[:-3]
    return gains


bot = discord.Bot()


bob = bot.create_group("bob", "Get Bells of Byelen data")
cota = bot.create_group("cota", "Get Call of the Armor data")
cromar = bot.create_group("cromar", "Get info about Cromar Bot")

current_ids = [1039354532167176303, 828646591471550474, 1030675539314352252]

@cromar.command(description="Get information about Cromar Bot.") # this decorator makes a slash command
async def help(ctx): # a slash command will be created with the name "ping"
    unitembed=discord.Embed(title="Available commands", color=0xac6c6c)
    unitembed.add_field(name='/bob unit [name]', value="Get Bells of Byelen unit data", inline=False)
    unitembed.add_field(name='/bob item [name]', value="Get Bells of Byelen item data", inline=False)
    unitembed.add_field(name='/bob skill [name]', value="Get Bells of Byelen skill data", inline=False)
    await ctx.response.send_message(embed=unitembed)


 #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@bob.command(description = "Get Bells of Byelen unit data")
async def unit(ctx, name: str):
    with open('bob unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            if(row['Name'].lower() == name.lower()):
                #await interaction.response.send_message("Name: " + row["Name"] + " HP Growth:" + row["HP Growth"])
                unitembed=discord.Embed(title=name.capitalize(), color=0xac6c6c)
                if (name.lower() == 'cromar' and random.randint(1, 10) == 1):
                    unitembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1043928901610643456/1080640506473762927/CromarFoggingOutknabepicer_1_1.png')
                    unitembed.add_field(name="Lv " + row['Lv'] + " ", value='Slayer', inline=True)
                elif (name.lower() == 'sera' and random.randint(1,10) == 1):
                    unitembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1043928901610643456/1080644681379106846/SeraZoomingRozeknabepicer_1.png')
                    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
                else:
                    unitembed.set_thumbnail(url=row['Portrait'])
                    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
                
                unitembed.add_field(name="PCC: ", value=row['PCC'], inline=True)
                unitembed.add_field(name="Movement Stars: ", value=row['Vigor'], inline=True)
                unitembed.add_field(name="Leadership: ", value=row['Leadership'], inline=True)
                bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] + " | " + "Mag " + row['Mag']+ " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Bld " + row['Bld'] + " | " + "Mov " + row['Mov']
                unitembed.add_field(name="Bases", value=bases, inline=False)
                growths = "HP " + row['HP Growth'] + "% | " + "Str " + row['Str Growth'] + "% | " + "Mag " + row['Mag Growth']+ "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "% | " + "Bld " + row['Bld Growth'] + "% | Mov " + row['Mov Growth'] + "%"
                unitembed.add_field(name="Growths", value=growths, inline=False)
                ranks = bob_get_ranks(row)
                unitembed.add_field(name="Ranks", value=ranks, inline=False)
                if (row['Skills'] != "None"):
                    unitembed.add_field(name="Skills", value=row['Skills'], inline=False)
                if (row['Promotes'] == "Yes"):
                    gains = bob_get_gains(row)
                    unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
                await ctx.response.send_message(embed=unitembed)
                was_found = True
        if (not was_found):
            await ctx.response.send_message("That unit does not exist.")


@bob.command(description = "Get Bells of Byelen item data")
async def item(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    if (stripped_name.lower() == 'axle'):
        await ctx.response.send_message("For Axel's Axle, search 'Axle1'. For Alex's Axle, search 'Axle2'.")  
    else:             
        with open('bob item.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            was_found = False
            for row in reader:
                if(row['Name'].lower() == stripped_name.lower()):
                    unitembed=discord.Embed(title=row['Display Name'], color=0xac6c6c)
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
            if (not was_found):
                await ctx.response.send_message("That item does not exist.")

@bob.command(description = "Get Bells of Byelen skill data")
async def skill(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('bob skill.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                unitembed=discord.Embed(title=row['Name'], color=0xac6c6c)
                unitembed.add_field(name='Description: ', value=row['Description'], inline=False)
                was_found = True
                await ctx.response.send_message(embed=unitembed)
        if (not was_found):
                await ctx.response.send_message("That skill does not exist.")




@cota.command(description = "Get Bells of Byelen unit data")
async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('cota unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                unitembed=discord.Embed(title=row['Name'], color=0xac6c6c)
                unitembed.set_thumbnail(url=row['Portrait'])
                unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
                unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
                bases = "HP " + row['HP'] + " | " + "Atk " + row['Atk'] + " | Skl" + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
                unitembed.add_field(name="Bases", value=bases, inline=False)
                growths = "HP " + row['HP Growth'] + "% | " + "Atk " + row['Atk Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
                unitembed.add_field(name="Growths", value=growths, inline=False)
                ranks = cota_get_ranks(row)
                unitembed.add_field(name="Ranks", value=ranks, inline=False)
                if (row['Promotes'] == "Yes"):
                    gains = cota_get_gains(row)
                    unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
                await ctx.response.send_message(embed=unitembed)
                was_found = True
        if (not was_found):
            await ctx.response.send_message("That unit does not exist.")



@bot.event
async def on_ready():
    print("Ready!")

token = ''
with open('token.txt') as f:
    token = f.read()

bot.run(token)