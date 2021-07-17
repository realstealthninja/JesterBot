import discord, os, requests, json, asyncio
from async_timeout import timeout
from random import choice, randint
from dutils import thecolor, Json, thebed
from discord.ext import commands 
from discord_components import DiscordComponents
from dislash import SlashClient, ActionRow, Button
import datetime
import shutil
selected_channel = None
   
class Staff(commands.Cog):
    def __init__(self, client):

        self.client = client

    @commands.command(hidden=True)
    async def abort(self, ctx):
        await thebed(ctx, '', 'Aborting')
        
        await self.client.close()
        os.system('python3 main.py')  

    @commands.command(hidden=True)
    async def drop(self, ctx):
        msg = await ctx.send(
            "This message has a select menu!",
            components=[
                SelectMenu(
                    custom_id="test",
                    placeholder="Choose up to 1 options",
                    max_values=1,
                    options=[
                        SelectOption("Option 1", "value 1"),
                        SelectOption("Option 2", "value 2"),
                        SelectOption("Option 3", "value 3")
                    ]
                )
            ]
        )
        print(dir(SelectMenu))
        def check(inter):
            return inter.message.id == msg.id and inter.author == ctx.author
        # Wait for someone to click on it
        inter = await msg.wait_for_dropdown(check)
        
        print(dir(inter))
        await inter.reply(f"Options: {inter.select_menu}")

    @commands.command(hidden=True)
    async def chelp(self, ctx):
        
          
        with open('./dicts/Cmds.json', 'r+') as e:
            j = 0
            data = json.load(e)
            for k in self.client.commands:
                if not k.hidden:

                    j += 1
            for k in self.client.walk_commands():   
                if not k.hidden:
                    if k.name not in data:
                        
                        await thebed(ctx, f"{k}", f'**{k.signature if k.signature else "no"}**  │  help cmd?', f=f"{len(data)} / {j}")
                        try:
                            received_msg = str((await self.client.wait_for('message', timeout=900.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                        except Asyncio.TimeoutError:
                            return
                        if received_msg == "end":
                            return
                        else:
                            data[k.name] = {
                                'help': received_msg
                            }
                            Json(e, data)
            await thebed(ctx, 'All done!')

    @commands.command(hidden=True)
    async def blacklist(self, ctx, user1:int, cmd):
       
            
        user = self.client.get_user(user1)
        command = self.client.get_command(cmd)
        with open('./dicts/Check.json', 'r+') as k:
            data = json.load(k)
            if str(user.id) in data:
                if cmd not in data[str(user.id)]['commands']:

                    data[str(user.id)]['commands'].append(command.name)
            else:
                data[str(user.id)] = {
                    'commands': [command.name]
                }
            Json(k, data)
    
        await thebed(ctx, 'done')
    @commands.command(hidden=True)
    async def rblacklist(self, ctx, user1:int, cmd):
       
        
        user = self.client.get_user(user1)
        command = self.client.get_command(cmd)
        with open('./dicts/Check.json', 'r+') as k:
            data = json.load(k)
            if str(user.id) in data:
                data[str(user.id)]['commands'].remove(command.name)
            
                
                Json(k, data)
    
        await thebed(ctx, 'done')
    @commands.command(hidden=True)
    async def newup(self, ctx):
    
        try:
            embed = discord.Embed(title="Version?")
            await ctx.send(embed=embed)
            ver = await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            with open('./dicts/Updates.json', 'r+') as k:
                loaded1 = json.load(k)
                for m in loaded1:
                    if str(m) not in loaded1:
                        pass    
                    else:
                        loaded1[m]["Version"] = ver.content
                            
                            




                        

                        k.seek(0)
                        k.truncate(0)  # clear previous content
                        k.write(json.dumps(loaded1, indent=4)) # write to file
            embed = discord.Embed(title="Bug fixes")
            await ctx.send(embed=embed)
            y = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
            while y not in  ["apply", "q"]:
                embed1 = discord.Embed(title="Bug fixes")
                await ctx.send(embed=embed1)



            
                
                with open('./dicts/Updates.json', 'r+') as k:
                    loaded1 = json.load(k)
                    for m in loaded1:
                        if str(m) not in loaded1:
                            pass    
                        else:
                            loaded1[m]["Bug fixes"] += f"\n- {y}"  

                            k.seek(0)
                            k.truncate(0)  # clear previous content
                            k.write(json.dumps(loaded1, indent=4)) # write to file
                y = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
            else:
                embed2 = discord.Embed(title="New commands")
                await ctx.send(embed=embed2)
                z = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                while z not in  ["apply", "q"]:
                    embed3 = discord.Embed(title="New commands")
                    await ctx.send(embed=embed3)


                
                    
                    with open('./dicts/Updates.json', 'r+') as k:
                        loaded1 = json.load(k)
                        for m in loaded1:
                            if str(m) not in loaded1:
                                pass    
                            else:
                                loaded1[m]["New commands"] += f"\n- {z}"  

                                k.seek(0)
                                k.truncate(0)  # clear previous content
                                k.write(json.dumps(loaded1, indent=4)) # write to file
                    
                    
                    z = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                else:
                    embed = discord.Embed(title="Other")
                    await ctx.send(embed=embed)
                    a = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                    while a not in  ["apply", "q"]:
                        embed3 = discord.Embed(title="Other")
                        await ctx.send(embed=embed3)


                    
                        
                        with open('./dicts/Updates.json', 'r+') as k:
                            loaded1 = json.load(k)
                            for m in loaded1:
                                if str(m) not in loaded1:
                                    pass    
                                else:
                                    loaded1[m]["Other"] += f"\n- {a}"  

                                    k.seek(0)
                                    k.truncate(0)  # clear previous content
                                    k.write(json.dumps(loaded1, indent=4)) # write to file
                        a = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                    else:
                        embed4 = discord.Embed(title="Applied")
                        await ctx.send(embed=embed4)
                        
                            
                            
                        
                            

                    
                
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Time ran out, restart the ticket", colour=thecolor())
            await ctx.send(embed=embed)


    @commands.command(hidden=True)
    async def newver(self, ctx, *, Destroy=""):
        
        if Destroy == "":
            with open('./dicts/Updates.json', 'r+') as k:
                loaded1 = json.load(k)
                for m in loaded1:
                    if str(m) not in loaded1:
                        pass    
                    else:
                        loaded1[m] = {
                            "Version": "",
                            "Bug fixes": "",
                            "New commands": "",
                            "Other": ""




                        } 

                        k.seek(0)
                        k.truncate(0)  # clear previous content
                        k.write(json.dumps(loaded1, indent=4)) # write to file
                        embed4 = discord.Embed(title="Applied")
                        await ctx.send(embed=embed4)
        else:           
            with open('./dicts/Updates.json', 'r+') as k:
                loaded1 = json.load(k)
                for m in loaded1:
                    if str(m) not in loaded1:
                        pass    
                    else:
                        loaded1[m][f"{Destroy}"] = ""

                        k.seek(0)
                        k.truncate(0)  # clear previous content
                        k.write(json.dumps(loaded1, indent=4)) # write to file
                        embed3 = discord.Embed(title="Applied")
                        await ctx.send(embed=embed3)


    @commands.command(hidden=True)
    async def balded(self, ctx):
        
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            await ctx.send(data)
            for key in data:
            
                if "Bal" in data[key]:
                    await ctx.send(key)

                    x = self.client.get_user(int(key))
                    if not x:
                        pass
                    else:

                        data[key]['Name'] = x.name
                        
                        Json(k, data)
                        await ctx.send(data[key]['Name'])
                else:
                    pass
        

    @commands.command(hidden=True)
    async def baladd(self, ctx, bal:int):
       
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            await ctx.send(data)
            for key in data:
            
                if "Bal" in data[key]:
                    await ctx.send(key)

                    x = self.client.get_user(int(key))
                    if not x:
                        pass
                    else:

                        data[key]['Bal'] += bal
                        
                        Json(k, data)
                        await ctx.send(data[key]['Bal'])
                else:
                    pass
    
    @commands.command(hidden=True)
    async def removefile(self, ctx, filed, dicte:str):
    
        with open(f'./dicts/{filed}', 'r+') as k:

        
            
            data = json.load(k)
            
        
            await ctx.send(data)

            for key in data:
                await ctx.send(key)
                await ctx.send(data[dicte])
                await ctx.send(dicte)
                if dicte == key:
                    del data[dicte]
                    Json(k, data)
  

    
    

    @commands.command(hidden=True)
    async def data(self, ctx, file1="", data1="", data2="", int1='False', *, add=""):
        if int1 == 'True':
            add = int(add)
            
        else:
            pass

        x = []
        y = []
     
       
        if not file1:
            for file1 in os.listdir('./dicts/'):
                    if file1.endswith('.json'):
                    
                        x.append(f"`{file1[:-5]}`")
            embed = discord.Embed(title="Files", description=", ".join(x), colour=thecolor())
            await ctx.send(embed=embed)
            
                
                
                        
    
            
        else:
            if not data1:

                with open(f"./dicts/{file1}.json", 'r+') as k:
                    data = json.load(k)
                    the_num = ''
                    for key in data:
                        
                        if len(key) == len('483631842554019841'):
                            try:

                                the_num = self.client.get_user(int(key))
                            except:

                                if not the_num:

                                    y.append(f"`{key}` │")
                            else:
                                y.append(f"`{key}: {the_num}` │")
                        else:
                            y.append(f"`{key}`")
                    embed = discord.Embed(description=", ".join(y))
                    await ctx.send(embed=embed)
                
                
                
                
            else:
                with open(f"./dicts/{file1}.json", 'r+') as k:
                    data = json.load(k)
                    if data1 in data:
                        if not data2:
                            embed = discord.Embed(description=data[data1])
                            await ctx.send(embed=embed)
                    
                        else:
                            data[data1][data2] = add
                            await ctx.send('yessir')
                            Json(k, data)
                        
                        

                        

                    else:
                        
                            
                        for key in data:
                            y.append(f"`{key}`")
                        embed = discord.Embed(description=", ".join(y))
                        await ctx.send(embed=embed)
                        
                

        

    @commands.command(hidden=True)
    async def serversin(self, ctx):
   
        x = []
        num = 0
        for g in self.client.guilds:
            x.append(g.name)
            num += 1
            
       
        await ctx.send(", ".join(x[1:25]))
        await ctx.send(", ".join(x[26:len(x)]))

    @commands.command(hidden=True)
    async def showcmds(self, ctx):
        x = []
        embed = discord.Embed(color=discord.Color.green())
        for command in self.client.commands:
            
            x.append(f"`{command.name}`")
        xnum = 0
        for i in range(0, len(x)):
            xnum += 1
            if xnum == 25:
                if i <= 25:
                    embed.add_field(name=i, value=", ".join(x[0:i]), inline=False)
                else:

                    r = i - 25
                    embed.add_field(name=i, value=", ".join(x[r:i]), inline=False)
                
                xnum = 0
            
        await ctx.send(embed=embed)
    @commands.command(hidden=True)
    async def but(self, ctx):
        

        # Make a row of buttons
        row_of_buttons = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Green button",
                custom_id="green"
            ),
            Button(
                style=ButtonStyle.red,
                label="Red button",
                custom_id="red"
            )
        )
        # Send a message with buttons
        msg = await ctx.send(
            "This message has buttons!",
            components=[row_of_buttons]
        )
        # Wait for someone to click on them
        def check(inter):
            return inter.message.id == msg.id
        inter = await ctx.wait_for_button_click(check)
        
        button_text = inter.clicked_button.label
        await inter.reply(f"Button: {button_text}")
    @commands.command(hidden=True)
    async def but2(self, ctx):
        await ctx.channel.send("Context",components=[Button(style=ButtonStyle.blue, label="Test", custom_id="TTTT")]) #Blue button with button label of "Test"
        res = await self.client.wait_for("button_click") #Wait for button to be clicked
        print(res.user, dir(res))
        await res.respond(type=InteractionType.UpdateMessage, content=f'Button Clicked')
    @commands.command(hidden=True, aliases=['save', 'backup'])
    async def savebackup(self, ctx):
        x = 1
        for f in os.listdir('../backup'):
            if int(f[-3:]) > x:
                x = int(f[-3:])
            if int(x) >= 100:
                thefile = f'w{x+1}'
            elif int(x) >= 10:
                thefile = f'w0{x+1}'
            else:
                thefile = f'w00{x+1}'
        dirname = f'../backup/{thefile}'
        dirname1 = f'../backup/{thefile}/files'
        os.makedirs(dirname)
        os.makedirs(dirname1)


        for k in os.listdir('./dicts/'):
            if k not in ["Text.txt"]:
                shutil.copy(f'./dicts/{k}', dirname1)
                
        for t in os.listdir('./cogs/'):
            if t != "__pycache__":
                shutil.copy(f'./cogs/{t}', dirname)
        await thebed(ctx, 'success', f'you have made a new backup folder called *{dirname}*')
    @commands.command(hidden=True)
    async def file(self, ctx, file):
        await ctx.send(file=discord.File(f"./dicts/{file}"))
    @commands.command(hidden=True)
    async def thecog(self, ctx):
        for thecog in self.client.cogs:

            cog = self.client.get_cog(thecog)

            await ctx.send(thecog)
    @commands.command(hidden=True)
    async def thetest(self, ctx):
        with open('./dicts/Emoji.json', 'r+') as k:
            data = json.load(k)
            data['emojis'] = {
                "Fun": "😎", 
                "Games": "🎮",
                "Moderation": "⚠",
                "Misc": "🤔",
                "Botinfo": "ℹ",
                "Economy": "💰"



            }
            Json(k, data)
   
    @commands.command(hidden=True)
    async def formathelp(self, ctx):
        
        x = 0 
        xy = []
        with open('./dicts/Help.json', 'r+') as K:
            data = json.load(K)
            for key in data:
                await ctx.send(key)
                
                y = data[key]['Cmds'].split(", ")
                await ctx.send(y)

                for t in y:
                    xy.append(f"`{t}`")

                    x += 1
                    if x == len(y):
                        data[key]['Cmds'] = ", ".join(xy)
                        await ctx.send(xy)
                        x = 0
                        xy = []
                    
                   
                        Json(K, data)
            await ctx.send('done')
    @commands.command(hidden=True)
    async def t(self, ctx, d, t=""):
        await thebed(ctx, d, t)

    @commands.command(hidden=True)
    async def addcmd(self, ctx, name, *, cmd):
        with open('./dicts/Commands.json', 'r+') as k:
            data = json.load(k)
            if name in data:
                return await thebed(ctx, 'Already there mate')
            data[name] = {
                'code': cmd,
                'makecmd': f'@client.command()\nasync def {name}(ctx):'

            }
            Json(k, data)
            thecmd = f"{data[name]['makecmd']}\n    {data[name]['code']}"
            await thebed(ctx, thecmd)
            self.client.add_command(thecmd)

    @commands.command(hidden=True)
    async def tag(self, ctx, errornum:str=None):
        k = open('./dicts/Errors.json', 'r+')
        data = json.load(k) 
        if not errornum:
            try:

                return await thebed(ctx, '', ", ".join([e for e in data]))
            except:
                return await thebed(ctx, '', 'All clear!')
        try:
            data[errornum]
        except:
            return await thebed(ctx, '', 'Out of range') 
        await thebed(ctx, 'Error', f'''
       **error code** : `{errornum}`
        **author** : `{data[errornum]["author"]}`
        **error** : `{data[errornum]["error"]}`
        **cmd** : `{data[errornum]["command"]}`

        
        
        
        ''')
    @commands.command(hidden=True)
    async def resolve(self, ctx, errornum:str=None):
        k = open('./dicts/Errors.json', 'r+')
        data = json.load(k) 
        if not errornum:
            try:

                return await thebed(ctx, '', ", ".join([e for e in data]))
            except:
                return await thebed(ctx, '', 'All clear!')
        if errornum == "all":
            with open('./dicts/Errors.json', 'w') as e:
                json.dump({}, e)
                return await thebed(ctx, '', 'Done')
        try:
            data[errornum]
        except:
            return await thebed(ctx, '', 'Out of range') 
        m = await ctx.send(embed=discord.Embed(title='Error', description=f'''
    **error code** : `{errornum}`
    **author** : `{data[errornum]["author"]}`
    **error** : `{data[errornum]["error"]}`
    **cmd** : `{data[errornum]["command"]}`
    ''', color=thecolor()))
        await m.add_reaction('👍')
        reaction, user = await self.client.wait_for('reaction_add', check=lambda r, u: u == ctx.author)
        await thebed(ctx, '', 'Done')
        del data[errornum]
        Json(k, data)
        
        
def setup(client):
  client.add_cog(Staff(client))