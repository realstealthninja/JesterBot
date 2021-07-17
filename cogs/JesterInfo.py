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
import io
import textwrap
import contextlib
import shutil
from discord.ext.buttons import Paginator
from traceback import format_exception
from dutils import thecolor, Json, thebed
import time
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from dislash import SlashClient, ActionRow, Button, SelectMenu, SelectOption
from datetime import datetime
from sys import executable
from subprocess import call


class JesterInfo(commands.Cog):
    def __init__(self, client):

        self.client = client
    
   
   
    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        return await thebed(ctx, '', f"I've been Up since **{days}** Days, **{hours}** Hours, **{minutes}** Minutes, and **{seconds}** Seconds!")
   
    
        
    @commands.command(aliases=['Ver', 'versions'], description="Sends the version that the discord bot is currently on - Changes frequently as updates occur")
    async def version(self, ctx):
        with open('./dicts/Updates.json', 'r') as x:
            data = json.load(x)
            for m in data:

                embed = discord.Embed(title=f"{data[m]['Version']}", colour=thecolor())
                await ctx.send(embed=embed)
        
    @commands.command(aliases=['scoreover', 'Overallscore', 'Overall_score'], description="Sends the total number of commands used")
    async def score(self, ctx):
        with open('./dicts/Scoreoverall.json', 'r') as x:
            data = json.load(x)
            embed = discord.Embed(title=f"{data['Score']['Score1']}", colour=thecolor())
            await ctx.send(embed=embed)
        
    
    @commands.command(description="Sends information about my account")
    async def info(self, ctx, member: discord.Member = ""):
        embed = discord.Embed(title="Information", timestamp=ctx.message.created_at, colour=thecolor())
        if not member:
            member = ctx.author
        x = []
        
        username = member.name
        userip = member.id
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Name", value=f"{username}")
        embed.add_field(name="Id", value=f"{userip}")
        embed.add_field(name="Joined server at", value=f"{member.joined_at}")
        embed.add_field(name="Joined discord at", value=f"{member.created_at}")
        embed.add_field(name="Nitro", value=f"{member.premium_since}") 
        embed.add_field(name="Mobile", value=f"{member.is_on_mobile()}")
        for k in member.public_flags.all():
            x.append(f"`{k.name}`")
        embed.add_field(name="Flags", value=f"{', '.join(x)}")
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['Servers', 'ServerInfo', 'Server_Info'])
    async def server(self, ctx):
        channel= ctx.channel
        serverinvite = await channel.create_invite()
        serverid = ctx.guild.id
        servername = ctx.guild.name
        embed = discord.Embed(title="Your info", colour=0x4286ff)
        embed.add_field(name="Name", value=f"{servername}", inline=False)
        embed.add_field(name="Id", value=f"{serverid}", inline=False)
        embed.add_field(name="Invite", value=f"{serverinvite}", inline=False)
        # embed.add_field(name=)
        await ctx.send(embed=embed)

    

    @commands.command(aliases=['notes', 'patchnotes', 'Updates', 'Patch_Notes', 'PT', 'up'], description="Sends the most recent update to the bot")
    async def update(self, ctx):
        
        
        with open('./dicts/Updates.json', 'r') as x:
            data = json.load(x)

            for m in data:
            
                if data[m]['Version'] == "":
                    embed = discord.Embed(description="Updates is currently being updated, no data to send", colour=thecolor())
                    return await ctx.send(embed=embed)
                if data[m]['Bug fixes'] == "":
                    embed = discord.Embed(description="Updates is currently being updated, no data to send", colour=thecolor())
                    await ctx.send(embed=embed)
                if data[m]['New commands'] == "":
                    embed = discord.Embed(description="Updates is currently being updated, no data to send", colour=thecolor())
                    await ctx.send(embed=embed)
                if data[m]['Other'] == "":
                    embed = discord.Embed(description="Updates is currently being updated, no data to send", colour=thecolor())
                    await ctx.send(embed=embed)
                else:
                    username = self.client.get_user(828363172717133874)
                    embed = discord.Embed(title=f"**Updates**  \u200b <:Jesterinfo:863075610048987166>", description="*Everytime there is a new update it will be \nposted here along with a version update!*", colour=thecolor())
                    embed.add_field(value=f"{data[m]['Version']}",name = "**Version**", inline=True)
                    
                    embed.add_field(value=f"{data[str(m)]['Bug fixes']}",name = "**Bug fixes**", inline=False)
                    embed.add_field(value=f"{data[str(m)]['New commands']}",name = "**New commands**", inline=True)
                    embed.add_field(value=f"{data[str(m)]['Other']}", name= "**Other**", inline=False)
                    
                    
                    embed.set_footer(text=ctx.author.name, icon_url=username.avatar_url)
                    embed.set_thumbnail(url='https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif')
                    
                    await ctx.send(embed=embed)
       
   

    @commands.command(aliases=['selfruns', 'commandsused', 'Selfrun', 'Self_Score'], description="Sends the ammount of commands that you personally have ran")
    async def selfscore(self, ctx):
        with open('./dicts/Selfscore.json') as f:
            data = json.load(f)
            if str(ctx.author.id) in data:
                embed = discord.Embed(title=f"The ammount of commands you have ran are {data[str(ctx.author.id)]['selfscore']}", colour=thecolor())
                await ctx.send(embed=embed)
                

            
    # Giveawaytime.start()
    # @commands.command(aliases=['json'], description="Sends some of the json files being used, dm the coder for all the json files")
    # async def jsonfile(self, ctx):

    #     await ctx.send(file=discord.File("./dicts/Selfscore.json"))
    #     await ctx.send(file=discord.File("./dicts/Welcome.json"))
    #     await ctx.send(file=discord.File("./dicts/Scoreoverall.json"))
    
    #     await ctx.send(file=discord.File("./dicts/Reactionrole.json"))
    #     await ctx.send(file=discord.File("./dicts/Updates.json"))
    #     await ctx.send(file=discord.File("./dicts/Commandsused.json"))
    

    @commands.command(aliases=['binv', 'botinv'])
    async def invite(self, ctx):
        embed = discord.Embed(title=f"I am currently in {len(self.client.guilds)} servers!", description="[Official server](https://discord.gg/2654CuU3ZU) │ [Invite me!](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591)", colour = thecolor())
        
        embed.set_author(icon_url=ctx.author.avatar_url, name="Invite")

        await ctx.send(embed=embed)



    @commands.command(aliases=['commandtop', 'cmdtop', 'topcmd'])
    async def topcommands(self, ctx):
        score_list = []
        sorted_score_dict = {}
        
        x = []
        y = '\n'
        with open('./dicts/Commandsused.json') as k:
            embed = discord.Embed(colour=0x4286ff)
            embed.set_author(name="Top commands", icon_url=ctx.author.avatar_url)

            data = json.load(k)
            def get_key(item):
                return item[1]['score']
            sorted_scores = sorted(data.items(), key=get_key, reverse=True)[:11]
        
            for item in sorted_scores:
                
                x.append(f"{item[0]}: {item[1]['score']}")
                
                #embed.add_field(name=f"\u200b", value=f"**{item[0]}**: {item[1]['score']}", inline=False)
            embed.add_field(name=f"\u200b", value=f"**{y.join(x)}**", inline=False)

            await ctx.send(embed=embed)

        
                




    @commands.command(aliases=['membtop', 'topmemb', 'memtop'], description="Sends the top members that have used the bot") 
    async def topmembers(self, ctx):
        score_list = []
        sorted_score_dict = {}
        
        x = []
        y = '\n'
        with open('./dicts/Selfscore.json') as k:
            embed = discord.Embed(colour=0x4286ff)
            embed.set_author(name="Top members", icon_url=ctx.author.avatar_url)
            data = json.load(k)
            def get_key(item):
                return item[1]['selfscore']
            sorted_scores = sorted(data.items(), key=get_key, reverse=True)[:11]
            
            for item in sorted_scores:
                for datas in data:
                    if item[0] in datas:
                        
                        name = data[datas]['Name']
                x.append(f"{name}: {item[1]['selfscore']}")
                
                #embed.add_field(name=f"\u200b", value=f"**{item[0]}**: {item[1]['score']}", inline=False)
            embed.add_field(name=f"\u200b", value=f"**{y.join(x)}**", inline=False)

            await ctx.send(embed=embed)


    @commands.command(aliases=['lengthcmd', 'cmdamm'])
    async def lengthcommand(self, ctx):
        num = 0
        for n in self.client.commands:
            if not n.hidden:
                num += 1

        embed = discord.Embed(title=f"The bot has {num} commands", color=thecolor())
        await ctx.send(embed=embed)


    @commands.command(description="States the developer of the JesterBot")
    async def coder(self, ctx):
        user = self.client.get_user(298043305927639041)
        if user in ctx.guild.members:

            embed = discord.Embed(description=f"{user.mention} is the creator", colour=thecolor())
        
        else:
            embed = discord.Embed(title=f"{user.name} is the creator", colour=thecolor())

        await ctx.send(embed=embed)


   
    
    @commands.command(aliases=['pin', 'pingy', 'ms', 'Latency'], description="Sends the ping of the bot")
    async def ping(self, ctx):
        embed = discord.Embed(description=f"My current ping is **{round(self.client.latency * 500)}** ms", colour=thecolor())
        y = 0
        for m in self.client.guilds:
            for e in m.members:
                y += 1
        embed.set_footer(text=f"Servers in: {len(self.client.guilds)} │ Overall users: {y}")
        await ctx.send(embed=embed)
    @commands.command(aliases=['pref', 'prefixs', 'pre', 'prefixes'], description="Change the prefix of the bot for you personally")
    async def prefix(self, ctx, *, prefix=None):
        if not prefix:
            x = []
            us = self.client.user
            async with ctx.typing():
                response = requests.get('https://official-joke-api.appspot.com/random_joke')
                fox = response.json()
                foxupdate = (fox["setup"]) 
                foxupdatey = (fox["punchline"])
                prefix = await self.client.get_prefix(ctx.message)
                for pref in prefix:
                    x.append(f"`{pref}`")
                embed = discord.Embed(title=f"Hello {ctx.author.name}", description=f"""
                │ My default prefix is: `^` │
                │ My prefix for you is: {', '.join(x)} │ 
                │ Type `^prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
                
                
                
                """, colour=thecolor())
                embed.set_author(name="JesterBot", icon_url=us.avatar_url)
        
                embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
                embed.set_footer(text="You can get more of these jokes with ^joke!")
            return await ctx.send(embed=embed)
        prefix = prefix.split(" ")
       
        print(prefix)
        if prefix:
        
            with open('./dicts/prefixes.json', 'r+') as e:
                data = json.load(e)
                if ctx.guild.id in data:
                    data[str(ctx.author.id)]['prefix'] = prefix

                else:
                    data[str(ctx.author.id)]= {
                        "prefix": prefix


                    }
                Json(e, data)
            prefix1 = []
            for num in prefix:
                prefix1.append(f"`{num}`")
            embed = discord.Embed(description=f"New prefix is {', '.join(prefix1) if prefix else f'{prefix1}'}!, ping me for my prefixes if you forget!", colour=thecolor())
            embed.set_author(icon_url=ctx.author.avatar_url, name="Prefix")
            await ctx.send(embed=embed)

    

   
    
    @commands.command()
    async def credits(self, ctx):
        coder = self.client.get_user(298043305927639041)
        ideas_designer = self.client.get_user(780555299106586634)
        helper = self.client.get_user(483631842554019841)
        helper2 = self.client.get_user(652407551849267200)
        sales = self.client.get_user(521226389559443461)
        designer = self.client.get_user(427120167361708032) 
        embed = discord.Embed(title="Credits", description=f"""
        **Coder:** *{coder.name}*
        **Designer:** *{designer.name}*
        **Helpers:** *{helper.name}*, *{helper2.name}*
        **Sales/Promoter:** *{sales.name}*
        **Ideas/layout designer:** *{ideas_designer}*
        
        
        
        
        """, color=thecolor())
        await ctx.send(embed=embed)
   
    @commands.command(aliases=['colour'], description="change the color of the embeds!")
    async def color(self, ctx, *, args):
        if args.startswith('0x') and len(args) == 8:
            with open('./dicts/Color.json', 'r+') as k:
                data = json.load(k)
                data['Color']['color'] = args
                Json(k, data)
                embed = discord.Embed(title='changed', color=int(args, 16))
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Color", description='Put `0x` infront of the six letter/number [color](https://www.color-hex.com/)', colour=thecolor())
            await ctx.send(embed=embed)
    
            


def setup(client):
  client.add_cog(JesterInfo(client))