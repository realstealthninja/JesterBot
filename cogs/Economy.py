import discord, os, requests, json, asyncio
from discord.ext.commands import has_permissions
from discord.ext import commands 
from discord.utils import get
from discord.ext import tasks
from discord import Intents
from asyncio import sleep
import yfinance as yf
from traceback import print_exc
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from random import choice, randint
from dutils import thecolor, Json, thebed
FALSCH = False
class Economy(commands.Cog):
    def __init__(self, client):

        self.client = client
    async def cog_after_invoke(self, ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) not in data:
                data[str(ctx.author.id)] = {
                    "Bal": 1,
                    "Name": ctx.author.name


                }
            else:
                x = randint(1, 10)
                data[str(ctx.author.id)]['Bal'] += x
            Json(k, data)
    
    @commands.group(aliases=['buy'], description="If `purchase` is empty, sends what can be bought, or if [`purchase`] is a purchasable you buy the item", invoke_without_command=True)
    async def shop(self, ctx, purchase=""): 
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if purchase == "":
                embed = discord.Embed(colour=thecolor())
                embed.set_author(icon_url=ctx.author.avatar_url, name="Shop")
                embed.add_field(name="\u200b", value=f"""
                **What you can purchase...** 

                - Custom role (`^buy role`), you choose the name and color! - `3000$.` 
                - Lucky box! (`^buy box`), you can buy and open a lucky box that can contain up to 300$! - `200$`
                - A gun (`^buy gun`), you can use a gun to steal a huge chunk of someones money! - `2000$`
                - A bag (`^buy bag`), the ability to rob someone for a small/medium ammount of money - `500$`
                - A portable corona virus (`^buy corona`), gives someone covid for 5 hours - meaning that work is disabled - `300$`

                **How to get money?**
                Everytime you run a command you get money, and there are also other commands you can run to get money;
                    : `gamble`
                    : `beg`
                    : `work`
                    : every time you run an economy command you also get from `1-10`$
                
                Your balance is: **{data[str(ctx.author.id)]['Bal']}$**""")
                await ctx.send(embed=embed)
    
    @shop.command() 
    async def role(self, ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if data[str(ctx.author.id)]['Bal'] > 1000:
                try:
                    
                    embed1 = discord.Embed(description = f"What would you like the name of your role to be", colour=thecolor())   
                    embed1.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed=embed1)
                    msg = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60.0)).content).lower()
                    embed1 = discord.Embed(description = f"What would you like the colour of your role to be? [Refer to this](https://www.color-hex.com/) \nAdd 0x infront of the color, e.g 0x4b46cd", colour=thecolor())   
                    embed1.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed=embed1)
                    msg1 = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60.0)).content).lower()
    
            
                    print(self, ctx)
                    role = await ctx.guild.create_role(name=msg, colour=int(msg1, 16))
        
                    

                    await ctx.author.add_roles(role)

                    embed1 = discord.Embed(title = f"Created!", colour=thecolor())   
                    embed1.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
                    await ctx.send(embed=embed1)
                    data[str(ctx.author.id)]['Bal'] -= 1000
                    Json(k, data)
                except asyncio.TimeoutError:
                    embed = discord.Embed(title="I gave up waiting", colour=thecolor())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You dont have enough money!", colour=thecolor())
                await ctx.send(embed=embed)
    @shop.command() 
    async def box(ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:

                if data[str(ctx.author.id)]['Bal'] >= 150:
                    
                    data[str(ctx.author.id)]['Bal'] -= 150
                    if "Box" in data[str(ctx.author.id)]:

                        data[str(ctx.author.id)]['Box'] += 1
                    else:
                        data[str(ctx.author.id)]['Box'] = 1

                    Json(k, data)
                    embed = discord.Embed(description=f"You bought a **lucky box**, to use it write `^open box`", colour=thecolor())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="You dont have enough money!", colour=thecolor())
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="You dont have enough money!", colour=thecolor())
                await ctx.send(embed=embed)

    @shop.command()
    async def gun(ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            i = str(ctx.author.id)
            if i in data and data[i]['Bal'] >= 2000:
                data[i]['Bal'] -= 2000
                if 'Gun' in data[i]:

                    data[i]['Gun'] += 1
                else:
                    data[i]['Gun'] = 1
                await thebed(ctx, 'Success', 'you have purchased your **gun**, but be careful! To use it type `^use gun`')
                Json(k, data)
            else:
                await thebed(ctx, "You don't have enough money!")

    @shop.command()
    async def bag(ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            i = str(ctx.author.id)
            if i in data and data[i]['Bal'] >= 500:
                data[i]['Bal'] -= 500
                if 'Bag' in data[i]:

                    data[i]['Bag'] += 1
                else:
                    data[i]['Bag'] = 1
                await thebed(ctx, 'Success', 'you have purchased your **bag**, to use it type `^use bag`')
                Json(k, data)
            else:
                await thebed(ctx, "You don't have enough money!")
       
    @shop.command(alises=['covid', 'cov'])
    async def corona(self, ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            with open('./dicts/Bal.json', 'r+') as k:
                data = json.load(k)
                i = str(ctx.author.id)
                if i in data and data[i]['Bal'] >= 300:
                    data[i]['Bal'] -= 300
                    if 'covid' in data[i]:

                        data[i]['covid'] += 1
                    else:
                        data[i]['covid'] = 1
                    await thebed(ctx, 'Success', 'you have purchased your portable covid, to use it type `^use corona`')
                    Json(k, data)
                else:
                    await thebed(ctx, "You don't have enough money!")

    @commands.command(aliases=['bal', 'money'], description="Sends the JesterCoins `[user] has, if no user specified it sends authors bal")
    async def balance(self, ctx, user:discord.Member=""):
        with open('./dicts/Bal.json') as k:
            data = json.load(k)
        

            if user == "":
                if str(ctx.author.id) in data:
                    embed = discord.Embed(description=f"**{data[str(ctx.author.id)]['Bal']}** JesterCoins", colour=thecolor())
                    embed.set_footer(text="Every time you run an economy command you get money!")
                    embed.set_author(icon_url=ctx.author.avatar_url, name="Balance")
                else:
                    embed = discord.Embed(description=f"You have 0$", colour=thecolor())
                    embed.set_author(icon_url=ctx.author.avatar_url, name="Balance")

            else:
                if str(user.id) in data:
                    embed = discord.Embed(description=f"{data[str(user.id)]['Bal']}$", colour=thecolor())
                else:
                    embed = discord.Embed(description=f"They have 0$", colour=thecolor())
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['bet', 'g'], description="Gambles the `<ammount>`, 1 in 3 chance to double money, 2 in 3 chance to lose the money you gambled...")
    async def gamble(self, ctx, money:int):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
            
        
    
                if money <= data[str(ctx.author.id)]['Bal']:
                    x = randint(1, 3)
                    if x == 1:

                        embed = discord.Embed(description = f"you gambled **{money}$** and got **{money * 2}$**", colour=thecolor())
                        embed.set_author(icon_url=ctx.author.avatar_url, name="You won!")
                        data[str(ctx.author.id)]['Bal'] += money * 2
                        Json(k, data)
                    else:
                        embed = discord.Embed(description = f"you gambled **{money}$** and lost **{money}$**", colour=thecolor())
                        embed.set_author(icon_url=ctx.author.avatar_url, name="You lost!")
                        data[str(ctx.author.id)]['Bal'] -= money 
                        Json(k, data)
                else:
                    embed = discord.Embed(description="You do not have enough money! type `^bal` to see your balance", colour=thecolor())
            else:
                embed = discord.Embed(title="You do not have enough money! type `^bal` to see your balance", colour=thecolor())

            await ctx.send(embed=embed)
    


    @commands.command(description="You get a random ammount of JesterCoins - 60 second cooldown!")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            x = randint(50, 200)
            data[str(ctx.author.id)]['Bal'] += x
            embed = discord.Embed(description=f"You begged and got **{x}** jestercoins!", colour=thecolor())
            await ctx.send(embed=embed)
            Json(k, data)


    @commands.command(aliases=['balancetop'], description="Sends the richest members")
    async def baltop(self, ctx):
        score_list = []
        sorted_score_dict = {}
        x1 = 0
        x = []
        y = '\n'
        with open('./dicts/Bal.json') as k:
            embed = discord.Embed(colour=thecolor())
            embed.set_author(name="Baltop", icon_url=ctx.author.avatar_url)
            data = json.load(k)
            def get_key(item):
                return item[1]['Bal']
            sorted_scores = sorted(data.items(), key=get_key, reverse=True)[:10]
            
            for item in sorted_scores:
                for datas in data:
                
                    if item[0] in datas:
                        x1 += 1
                        name = data[datas]['Name']
                x.append(f"**__{x1}. {name}__:**\n JesterCoins: {item[1]['Bal']}$")
                
                #embed.add_field(name=f"\u200b", value=f"**{item[0]}**: {item[1]['score']}", inline=False)
            embed.add_field(name=f"\u200b", value=f"{y.join(x)}", inline=False)

            await ctx.send(embed=embed)
        
    @commands.command(aliases=['give'], description="Sends the <ammount> from your bank to their bank!")
    async def gift(self, ctx, user:discord.Member, ammount:int):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if data[str(ctx.author.id)]['Bal'] >= ammount:
                

                if str(user.id) in data:
                    data[str(user.id)]['Bal'] += ammount
                    
                    data[str(ctx.author.id)]['Bal'] -= ammount
                    Json(k, data)
                    embed = discord.Embed(description=f"You sent to **{ammount}$** to {user.name}!", colour=thecolor())
                else:
                    data[str(user.id)] = {
                        "Bal": ammount,
                        "Name": user.name

                    }
                    data[str(ctx.author.id)]['Bal'] -= ammount
                    Json(k, data)
                    embed = discord.Embed(description=f"You sent to **{ammount}$** to {user.name}!", colour=thecolor())           
            else:
                embed = discord.Embed(description=f"You don't have {ammount}! Type `^bal` for your balance!", colour=thecolor())
            await ctx.send(embed=embed)
    @commands.command(aliases=['givehide'], description="Sends the <ammount> from your bank to their bank!", hidden=True)
    async def gifthide(self, ctx, user:int, ammount:int):
   
        user = self.client.get_user(user)
    
        if user:
            if ctx.author.id == 298043305927639041:
                with open('./dicts/Bal.json', 'r+') as k:
                    data = json.load(k)
                    if data[str(ctx.author.id)]['Bal'] >= ammount:
                        

                        if str(user.id) in data:
                            data[str(user.id)]['Bal'] += ammount
                            Json(k, data)
                            
                            embed = discord.Embed(description=f"You sent to {ammount}$ to {user.name}!", colour=thecolor())
                        else:
                            data[str(user.id)] = {
                                "Bal": ammount,
                                "Name": user.name

                            }
                
                            Json(k, data)
                            embed = discord.Embed(description=f"You sent to {ammount}$ to {user.name}!", colour=thecolor())           
                    else:
                        embed = discord.Embed(description=f"You don't have {ammount}! Type `^bal` for your balance!", colour=thecolor())
                    await ctx.send(embed=embed)
        else:
            await ctx.send("no")
    @commands.group(aliases=['open', 'use'], description="unlocks your Lucky boxes!", invoke_without_command=True)
    async def unlock(self, ctx, what=""):
        await thebed(ctx, '', 'Type what you want to open! Type `^inv` to see what you have available to unlock! To buy unlockable items type `^shop`')

    @unlock.group()
    async def box(self, ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                if data[str(ctx.author.id)]['Box'] >= 1:
                    rand_prize = randint(200, 300)
                    data[str(ctx.author.id)]['Box'] -= 1
                    data[str(ctx.author.id)]['Bal'] += rand_prize
                    Json(k, data)
                    embed = discord.Embed(description=f"You got **{rand_prize}**$!", colour=thecolor())
                    await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(title="You dont have a lucky box! Type `^shop box` to buy one!", colour=thecolor())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You dont have a lucky box! Type `^shop box` to buy one!", colour=thecolor())
                await ctx.send(embed=embed)
    # @unlock.group(aliases=['cov', 'corona'])
    # async def covid(self, ctx, user:discord.Member=""):
    #     if not user and user != ctx.author:
    #         return await thebed(ctx, 'You need to mention someone to rob!')
    #     with open('./dicts/Bal.json', 'r+') as k:
    #         data = json.load(k)
    #         if str(ctx.author.id) in data:
    #             if 'covid' in data[str(ctx.author.id)]:
                    
                    
    #                 data[str(ctx.author.id)]['covid'] -= 1
    #                 Json(k, data)
    #                 embed = discord.Embed(description=f"Success!", colour=thecolor())
    #                 await ctx.send(embed = embed)
    #                 await asyncio.sleep(3600)
                    

                    
    #                 Json(k, data)
                    
                    
    #             else:
    #                 embed = discord.Embed(title="You dont have a porta-covid! Type `^shop covid` to buy one!", colour=thecolor())
    #                 await ctx.send(embed=embed)
    #         else:s
    #             embed = discord.Embed(title="You dont have a porta-covid! Type `^shop covid` to buy one!", colour=thecolor())
    #             await ctx.send(embed=embed)
    @unlock.group()
    async def bag(self, ctx, user:discord.Member=""):
        if not user and user != ctx.author:
            return await thebed(ctx, 'You need to mention someone to rob!')
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                if 'Bag' in data[str(ctx.author.id)]:
                    if data[str(ctx.author.id)]['Bag'] >= 1:
                        rand_prize = randint(200, 300)
                        data[str(ctx.author.id)]['Bag'] -= 1
                        if str(user.id) in data and data[str(user.id)]['Bal'] >= 100:
                            ran = randint(100, data[str(user.id)]['Bal'])
                        
                            data[str(ctx.author.id)]['Bal'] += ran
                            data[str(user.id)]['Bal'] -= ran
                            Json(k, data)
                            embed = discord.Embed(description=f"You robbed **{ran}**$!", colour=thecolor())
                            await ctx.send(embed = embed)
                            

                        else:
                            await thebed(ctx, 'They dont have enough in their bank!')

                    else:
                        embed = discord.Embed(title="You dont have a bag! Type `^shop bag` to buy one!", colour=thecolor())
                        await ctx.send(embed=embed)

                        
                else:
                    embed = discord.Embed(title="You dont have a bag! Type `^shop bag` to buy one!", colour=thecolor())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You dont have a bag! Type `^shop bag` to buy one!", colour=thecolor())
                await ctx.send(embed=embed)
    @unlock.group()
    async def gun(self, ctx, user:discord.Member=""):
        if not user and user != ctx.author:
            await thebed(ctx, 'You need to mention someone to rob!')
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                if data[str(ctx.author.id)]['gun'] >= 1:
                    rand_prize = randint(200, 300)
                    data[str(ctx.author.id)]['gun'] -= 1
                    if str(user.id) in data and data[str(user.id)]['Bal'] >= 300:
                        ran = randint(300, data[str(user.id)]['Bal'])
                    
                        data[str(ctx.author.id)]['Bal'] += ran
                        data[str(user.id)]['Bal'] -= ran
                        Json(k, data)
                        embed = discord.Embed(description=f"You robbed **{ran}**$!", colour=thecolor())
                        await ctx.send(embed = embed)
                        

                    else:
                        await thebed(ctx, 'They dont have enough in their bank!')
                    
                    
                    
                else:
                    embed = discord.Embed(title="You dont have a gun! Type `^shop gun` to buy one!", colour=thecolor())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You dont have a gun! Type `^shop gun` to buy one!", colour=thecolor())
                await ctx.send(embed=embed)

    @commands.command(aliases=['inv'], description="Sends your current inventory")
    async def inventory(self, ctx):
        with open('./dicts/Bal.json') as k:
            embed = discord.Embed(title="Your inventory is currently:", colour=thecolor())
            
            data = json.load(k)
            if str(ctx.author.id) in data:
                for b in data[str(ctx.author.id)]:
                    if b != "Name":

                        embed.add_field(name=f"{b}", value=f"{data[str(ctx.author.id)][b]}", inline=False)
            
                await ctx.send(embed=embed) 
            else:
                embed = discord.Embed(title="Your inv is empty currently!", colour=thecolor())
                await ctx.send(embed=embed) 

 
    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user) 
    async def work(self, ctx):
        with open('./dicts/Bal.json', 'r+') as k:
            
            data = json.load(k)
            if FALSCH == True:
                return await thebed(ctx, '', 'You cannot work! You have got covid')
            mon = data[str(ctx.author.id)]['Bal']
            x = randint(250, 750)
            mon += x 
            l = [
                "maid",
                "prostitute",
                "taxi driver",
                "cleaner",
                "trash cleaner",
                "coder",
                "programmer",
                "truck driver",
                "shop keeper",
                "alchoholic (the government was handing out free money)",
                "farmer",
                "blacksmith",
                "artist",
                "product tester",
                "designer",
                "architect",
                "teacher",
                "lawyer",
                "soldier",
                "police officer",
                "plumber",
                "handyman",
                "psychiatrist",
                "therapist",
                "athlete",
                "wrestler",
                "sales managment",
                "fisherman",
                "lumberjack",
                "insurance provider",
                "doctor",
                "nurse",
                "actuary",
                "barrister",
                "scientist",
                "curator",
                "herbalist",
                "broker",
                "banker",
                "journalist",
                "analyst",
                "it consultant",
                "museum guide tour",
                "miner",
                "pharmacist",
                "musician",
                "librarian",
                "site manager",
                "trader",
                "translator"







            ]
            v = ""
            e = choice(l)
            if e[:1] in ['a', 'e', 'i', 'u', 'o']:
                v = f"an {e}"
            else:
                v = f"a {e}"


            Json(k, data)
            await thebed(ctx, 'Work', f'''
            
            
            You just made `{x}` JesterCoins from working as {v}
            
            ''')
   
def setup(client):
  client.add_cog(Economy(client))