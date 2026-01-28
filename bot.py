import discord
import csv
import re
import random
import Cota.cota
import tlp.tlp
import sevensibs.sevens
import bob.bob
import trtr.trtr
import vq.vq
import vba.vba
import fourkings.fourkings
import dow.dow
import sp.sp
import dlatmol.dlatmol
import burger.burger
import ee.ee
import fehr.fehr
import john.john
import don.don
import avt.avt
import oc.oc
import auc.auc
import cc.cc
import tmgc.tmgc
import dof.dof
import dh.dh
import lots.lots
import hag.hag
from discord.ext import commands
from discord import option
import sys

bot = discord.Bot()

#cota = cromar.create_subgroup("cota", "Get Call of the Armor data")

test_ids = [1039354532167176303]
public_test_ids = [1039354532167176303,1081749141480288256]

@bot.command(description="Call Cromar Bot and get a response.")
@option("input", description = "Format is [command] [hack] [name]")
async def cromar(ctx, input: str):
    if (input == 'help'):
        await help(ctx)
    else: 
        parsedInput = input.split(" ", 2)
        command = parsedInput[0]
        hack = parsedInput[1]
        name = parsedInput[2]
        if (command == "unit"):
            await unit(ctx, hack, name)
        elif (command == "item"):
            await item(ctx, hack, name)
        elif (command == "skill"):
            await skill(ctx, hack, name)
        elif (command == "boss"):
            await boss(ctx, hack, name)
        else:
            await ctx.response.send_message("That command does not exist.")

async def help(ctx): 
    unitembed=discord.Embed(title="Available commands", color=0x676b68)
    unitembed.add_field(name='Invite Link', value='https://discord.com/api/oauth2/authorize?client_id=1039342081245724723&permissions=277025672192&scope=bot', inline=False)
    unitembed.add_field(name="Hack Abbreviations", value="https://github.com/knabepicer/CromarBot/blob/main/Hack%20abbreviations.txt",inline=False)
    unitembed.add_field(name='/cromar [command] [hack] [name]', value= "Alternative way to call bot- faster to type, but no autocorrect", inline=False)
    unitembed.add_field(name='/unit [hack] [name]', value="Get unit data - currently supports 4k, 7s, auc, avt, bob, burger, cc, cota, dlatmol, do5, dow, don, dh, ee, fehr, hag, john, lots, oc, sp, tlp, tmgc, trtr, vq, vba", inline=False)
    unitembed.add_field(name='/item [hack] [name]', value="Get item data - currently supports auc, bob, cc, don, oc", inline=False)
    unitembed.add_field(name='/skill [hack] [name]', value="Get skill data - currently supports bob, fehr, hag, vq", inline=False)
    unitembed.add_field(name='/boss [hack] [name]', value="Get boss data - currently supports burger, tlp", inline=False)
    
    await ctx.response.send_message(embed=unitembed)

async def get_unit_names(ctx: discord.AutocompleteContext):
    hack = ctx.options['hack']
    if (hack == 'cota'):
        return Cota.cota.get_unit_names(ctx)
    elif (hack == 'tlp'):
        return tlp.tlp.get_unit_names(ctx)
    elif (hack == '7s'):
        return sevensibs.sevens.get_unit_names(ctx)
    elif (hack == 'bob'):
        return bob.bob.get_unit_names(ctx)
    elif (hack == 'trtr'):
        return trtr.trtr.get_unit_names(ctx)
    elif (hack == 'rtr'):
        return trtr.trtr.get_unit_names(ctx)
    elif (hack == 'vq'):
        return vq.vq.get_unit_names(ctx)
    elif (hack == 'vba'):
        return vba.vba.get_unit_names(ctx)
    elif (hack == '4k'):
        return fourkings.fourkings.get_unit_names(ctx)
    elif (hack == 'dow'):
        return dow.dow.get_unit_names(ctx)
    elif (hack == 'sp'):
        return sp.sp.get_unit_names(ctx)
    elif (hack == 'dlatmol'):
        return dlatmol.dlatmol.get_unit_names(ctx)
    elif (hack == 'burger'):
        return burger.burger.get_unit_names(ctx)
    elif (hack == 'ee'):
        return ee.ee.get_unit_names(ctx)
    elif (hack == 'fehr'):
        return fehr.fehr.get_unit_names(ctx)
    elif (hack == 'john'):
        return john.john.get_unit_names(ctx)
    elif (hack == 'don'):
        return don.don.get_unit_names(ctx)
    elif (hack == 'avt'):
        return avt.avt.get_unit_names(ctx)
    elif (hack == 'oc'):
        return oc.oc.get_unit_names(ctx)
    elif (hack == 'auc'):
        return auc.auc.get_unit_names(ctx)
    elif (hack == 'cc'):
        return cc.cc.get_unit_names(ctx)
    elif (hack == 'tmgc'):
        return tmgc.tmgc.get_unit_names(ctx)
    elif (hack == 'do5'):
        return dof.dof.get_unit_names(ctx)
    elif (hack == 'dh'):
        return dh.dh.get_unit_names(ctx)
    elif (hack == 'lots'):
        return lots.lots.get_unit_names(ctx)
    elif (hack == 'hag'):
        return hag.hag.get_unit_names(ctx)
    else:
        return []
    


@bot.slash_command(description = "Get playable unit data")
@option("hack", description = "Name of the hack to get data for",
        autocomplete=discord.utils.basic_autocomplete(
        ["4k","7s","avt","auc","bob","burger","cota","cc","dlatmol","do5","don","dow","dh","ee","fehr","hag","john","lots","oc", "sp","tlp","tmgc","trtr","vba","vq"]
    ))
@option("name", description = "Name of the character to get data for", autocomplete=get_unit_names)
@option("levels", description = "For calculating average stats")
async def unit(ctx, hack: str, name: str, levels: str = None):
    if (hack == 'cota'):
        await Cota.cota.unit(ctx, name)
    elif (hack == 'tlp'):
        await tlp.tlp.unit(ctx, name)
    elif (hack == '7s'):
        await sevensibs.sevens.unit(ctx, name)
    elif (hack == 'bob'):
        await bob.bob.unit(ctx, name)
    elif (hack == 'trtr'):
        await trtr.trtr.unit(ctx, name)
    elif (hack == 'rtr'):
        await trtr.trtr.unit(ctx, name)
    elif (hack == 'vq'):
        await vq.vq.unit(ctx, name)
    elif (hack == 'vba'):
        await vba.vba.unit(ctx, name)
    elif (hack == '4k'):
        await fourkings.fourkings.unit(ctx, name)
    elif (hack == 'dow'):
        await dow.dow.unit(ctx, name)
    elif (hack == 'sp'):
        await sp.sp.unit(ctx, name)
    elif (hack == 'dlatmol'):
        await dlatmol.dlatmol.unit(ctx, name)
    elif (hack == 'burger'):
        await burger.burger.unit(ctx, name)
    elif (hack == 'ee'):
        await ee.ee.unit(ctx, name)
    elif (hack == 'fehr'):
        await fehr.fehr.unit(ctx, name)
    elif (hack == 'john'):
        await john.john.unit(ctx, name)
    elif (hack == 'don'):
        await don.don.unit(ctx, name)
    elif (hack == 'avt'):
        await avt.avt.unit(ctx, name)
    elif (hack == 'oc'):
        await oc.oc.unit(ctx, name)
    elif (hack == 'auc'):
        await auc.auc.unit(ctx, name)
    elif (hack == 'cc'):
        await cc.cc.unit(ctx, name)
    elif (hack == 'tmgc'):
        await tmgc.tmgc.unit(ctx, name)
    elif (hack == 'do5'):
        await dof.dof.unit(ctx, name)
    elif (hack == 'dh'):
        await dh.dh.unit(ctx, name)
    elif (hack == 'lots'):
        await lots.lots.unit(ctx, name)
    elif (hack == 'hag'):
        await hag.hag.unit(ctx, name, levels)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")


async def get_boss_names(ctx: discord.AutocompleteContext):
    hack = ctx.options['hack']
    if (hack == 'tlp'):
        return tlp.tlp.get_boss_names(ctx)
    elif (hack == 'burger'):
        return burger.burger.get_boss_names(ctx)
    else:
        return[]



@bot.slash_command(description = "Get boss unit data")
@option("hack", description = "Name of the hack to get data for",
        autocomplete=discord.utils.basic_autocomplete(
        ["tlp", "burger"]
    ))
@option("name", description = "Name of the character to get data for", autocomplete= get_boss_names)
async def boss(ctx, hack: str, name: str):
    if (hack == 'tlp'):
        await tlp.tlp.boss(ctx, name)
    elif (hack == 'burger'):
        await burger.burger.boss(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")

async def get_item_names(ctx: discord.AutocompleteContext):
    hack = ctx.options['hack']
    if (hack == 'bob'):
        return bob.bob.get_item_names(ctx)
    elif (hack == 'don'):
        return don.don.get_item_names(ctx)
    elif (hack == 'auc'):
        return auc.auc.get_item_names(ctx)
    elif (hack == 'oc'):
        return oc.oc.get_item_names(ctx)
    elif (hack == 'cc'):
        return cc.cc.get_item_names(ctx)
    else:
        return[]





@bot.slash_command(description = "Get item data")
@option("hack", description = "Name of the hack to get data for",
        autocomplete=discord.utils.basic_autocomplete(
        ["auc","bob", "cc","don", "oc"]
    ))
@option("name", description = "Name of the item to get data for", autocomplete = get_item_names)
async def item(ctx, hack: str, name: str):
    if (hack == 'bob'):
        await bob.bob.item(ctx, name)
    elif (hack == 'don'):
        await don.don.item(ctx, name)
    elif (hack == 'auc'):
        await auc.auc.item(ctx, name)
    elif (hack == 'oc'):
        await oc.oc.item(ctx, name)
    elif (hack == 'cc'):
        await cc.cc.item(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")



async def get_skill_names(ctx: discord.AutocompleteContext):
    hack = ctx.options['hack']
    if (hack == 'bob'):
        return bob.bob.get_skill_names(ctx)
    elif (hack == 'vq'):
        return vq.vq.get_skill_names(ctx)
    elif (hack == 'fehr'):
        return fehr.fehr.get_skill_names(ctx)
    elif (hack == 'hag'):
        return hag.hag.get_skill_names(ctx)
    else:
        return[]


@bot.slash_command(description = "Get skill data")
@option("hack", description = "Name of the hack to get data for",
        autocomplete=discord.utils.basic_autocomplete(
        ["bob", 'vq', 'fehr', 'hag']
    ))
@option("name", description = "Name of the skill to get data for", autocomplete=get_skill_names)
async def skill(ctx, hack: str, name: str):
    if (hack == 'bob'):
        await bob.bob.skill(ctx, name)
    elif (hack == 'vq'):
        await vq.vq.skill(ctx, name)
    elif (hack == 'fehr'):
        await fehr.fehr.skill(ctx, name)
    elif (hack == 'hag'):
        await hag.hag.skill(ctx, name)
    else:
        await ctx.response.send_message("That hack does not exist or is not supported by this command.")

#bot.load_extension("bob.bob")
#bot.load_extension("cota.cota")
#bot.load_extension("7s.sevens")
#bot.load_extension("trtr.trtr")
#bot.load_extension("tlp.tlp")
@bot.event
async def on_ready():
    
    print("Ready!")
   

token = ''
with open('token.txt') as f:
    token = f.read()

bot.run(token)