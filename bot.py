import discord
import csv


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
        gains += "Sword: " + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
        gains += "Lance: " + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
        gains += "Axe: " + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
        gains += "Bow: " + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
        gains += "Staff: " + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
        gains += "Anima: " + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
        gains += "Light: " + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
        gains += "Dark: " + row['Dark Gains'] + " | "
    gains = gains[:-3]
    return gains


bot = discord.Bot()


bob = bot.create_group("bob", "Get Bells of Byelen data")


 #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@bob.command(description = "Get Bells of Byelen unit data", guild_ids=[1039354532167176303])
async def unit(ctx, name: str):
    with open('bob unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            if(row['Name'].lower() == name.lower()):
                #await interaction.response.send_message("Name: " + row["Name"] + " HP Growth:" + row["HP Growth"])
                unitembed=discord.Embed(title=name.capitalize(), color=0xac6c6c)
                unitembed.set_thumbnail(url=row['Portrait'])
                unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
                unitembed.add_field(name="PCC: ", value=row['PCC'], inline=True)
                unitembed.add_field(name="Movement Stars: ", value=row['Vigor'], inline=True)
                unitembed.add_field(name="Leadership: ", value=row['Leadership'], inline=True)
                bases = "HP " + row['HP'] + " | " + "Str " + row['Str'] + " | " + "Mag " + row['Mag']+ " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Bld " + row['Bld'] + " | " + "Mov " + row['Mov']
                unitembed.add_field(name="Bases", value=bases, inline=False)
                growths = "HP " + row['HP Growth'] + " | " + "Str " + row['Str Growth'] + " | " + "Mag " + row['Mag Growth']+ " | Skl " + row['Skl Growth'] + " | " + "Spd " + row['Spd Growth'] + " | " + "Lck " + row['Luck Growth'] + " | " + "Def " + row['Def Growth'] + " | " + "Res " + row['Res Growth'] + " | " + "Bld " + row['Bld Growth'] + " | Mov " + row['Mov Growth']
                unitembed.add_field(name="Growths", value=growths, inline=False)
                ranks = bob_get_ranks(row)
                unitembed.add_field(name="Ranks", value=ranks, inline=False)
                unitembed.add_field(name="Skills", value=row['Skills'], inline=False)
                if (row['Promotes'] == "Yes"):
                    gains = bob_get_gains(row)
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