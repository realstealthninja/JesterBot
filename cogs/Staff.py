import disnake, os, requests, json, asyncio
from disnake.ext import commands 

import shutil   

from core.utils.utils import thecolor, Json, thebed
from core.Context import Context


class Staff(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
    
    @commands.command(hidden=True)
    async def push(self, ctx, reason):
        embed = disnake.Embed(title="Git push.", description="")
        git_commands = [
            ["git", "add", "."],
            ["git", "commit", "-m", reason],
            ["git", "push"],
        ]

        for git_command in git_commands:
            process = await asyncio.create_subprocess_exec(
                git_command[0],
                *git_command[1:],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            output, error = await process.communicate()
            embed.description += f'[{" ".join(git_command)!r} exited with return code {process.returncode}\n'

            if output:
                embed.description += f"**[stdout]**\n{output.decode()}\n"
            if error:   
                embed.description += f"**[stderr]**\n{error.decode()}\n"
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def pull(self, ctx):
        embed = disnake.Embed(title="Git pull.", description="")
        git_commands = [
            ["git", "stash"],
            ["git", "pull", "--ff-only"]
        ]

        for git_command in git_commands:
            process = await asyncio.create_subprocess_exec(
                git_command[0],
                *git_command[1:],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            output, error = await process.communicate()
            embed.description += f'[{" ".join(git_command)!r} exited with return code {process.returncode}\n'

            if output:
                embed.description += f"**[stdout]**\n{output.decode()}\n"
            if error:   
                embed.description += f"**[stderr]**\n{error.decode()}\n"
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def load(self, ctx: Context, extension):
        embed = disnake.Embed(color=disnake.Color.dark_gold())
        self.bot.load_extension(f'cogs.{extension}')
        embed.add_field(name="Load Extension", value=f"Loaded cog: ``{extension}`` successfully")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def wcog(self, ctx: Context, n):
        cmd = self.bot.get_command(n)
        await ctx.send(cmd.cog.qualified_name)
    @commands.command(hidden=True)
    async def unload(self, ctx: Context, extension):
            self.bot.unload_extension(f'cogs.{extension}')
            embed = disnake.Embed(color=disnake.Color.dark_gold())
            embed.add_field(name="Unload Extension", value=f"Unloaded cog: ``{extension}`` successfully")
            await ctx.send(embed=embed)

    @commands.command(aliases=['r'], hidden=True)
    async def reload(self, ctx: Context, extension=""):
        if not extension:
    
            for cog in tuple(self.bot.extensions):
                if cog[5:] not in ["Misc", "Economy", "Mod"]:
                    self.bot.reload_extension(cog)
            embed = disnake.Embed(color=disnake.Color.dark_gold())
            embed.add_field(name="Reload Extension", value=f"Reloaded cogs successfully")
            print('\n\n\n\nReloaded\n--------------------------------')
            await ctx.send(embed=embed)
        else:

            self.bot.reload_extension(f'cogs.{extension}')
            embed = disnake.Embed(color=disnake.Color.dark_gold())
            embed.add_field(name="Reload Extension", value=f"Reloaded cog: ``{extension}`` successfully")
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def abort(self, ctx: Context):
        
        await thebed(ctx, '', 'Aborting')
        
        await self.bot.close()
        os.system('python3 main.py')



    @commands.command(hidden=True)
    async def chelp(self, ctx: Context):
        with open('./dicts/Cmds.json', 'r+') as e:
            j = 0
            data = json.load(e)
            for k in self.bot.commands:
                if not k.hidden:

                    j += 1
            for k in self.bot.walk_commands():   
                if not k.hidden:
                    if k.name not in data:
                        
                        await thebed(ctx, f"{k}", f'**{k.signature if k.signature else "no"}**  │  help cmd?', f=f"{len(data)} / {j}")
                        try:
                            received_msg = str((await self.bot.wait_for('message', timeout=900.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                        except asyncio.TimeoutError:
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
    async def close(self, ctx: Context):

        embed = disnake.Embed(title=f"Goodbye", colour=thecolor())
        await ctx.send(embed=embed)
        
        await self.bot.close()

    

    @commands.command(hidden=True)
    async def blacklist(self, ctx: Context, user1:int, cmd):
       
            
        user = self.bot.get_user(user1)
        command = self.bot.get_command(cmd)
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
    async def rblacklist(self, ctx: Context, user1:int, cmd):
       
        
        user = self.bot.get_user(user1)
        command = self.bot.get_command(cmd)
        with open('./dicts/Check.json', 'r+') as k:
            data = json.load(k)
            if str(user.id) in data:
                data[str(user.id)]['commands'].remove(command.name)
            
                
                Json(k, data)
    
        await thebed(ctx, 'done')
    @commands.command(hidden=True)
    async def newup(self, ctx: Context):
    
        try:
            embed = disnake.Embed(title="Version?")
            await ctx.send(embed=embed)
            ver = await self.bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
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
            embed = disnake.Embed(title="Bug fixes")
            await ctx.send(embed=embed)
            y = str((await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
            while y not in  ["apply", "q"]:
                embed1 = disnake.Embed(title="Bug fixes")
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
                y = str((await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
            else:
                embed2 = disnake.Embed(title="New commands")
                await ctx.send(embed=embed2)
                z = str((await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                while z not in  ["apply", "q"]:
                    embed3 = disnake.Embed(title="New commands")
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
                    
                    
                    z = str((await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                else:
                    embed = disnake.Embed(title="Other")
                    await ctx.send(embed=embed)
                    a = str((await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                    while a not in  ["apply", "q"]:
                        embed3 = disnake.Embed(title="Other")
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
                        a = str((await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                    else:
                        embed4 = disnake.Embed(title="Applied")
                        await ctx.send(embed=embed4)
                        
                            
                            
                        
                            

                    
                
        except asyncio.TimeoutError:
            embed = disnake.Embed(title="Time ran out, restart the ticket", colour=thecolor())
            await ctx.send(embed=embed)


    @commands.command(hidden=True)
    async def newver(self, ctx: Context, *, Destroy=""):
        
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
                        embed4 = disnake.Embed(title="Applied")
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
                        embed3 = disnake.Embed(title="Applied")
                        await ctx.send(embed=embed3)


    @commands.command(hidden=True)
    async def balded(self, ctx: Context):
        
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            await ctx.send(data)
            for key in data:
            
                if "Bal" in data[key]:
                    await ctx.send(key)

                    x = self.bot.get_user(int(key))
                    if not x:
                        pass
                    else:

                        data[key]['Name'] = x.name
                        
                        Json(k, data)
                        await ctx.send(data[key]['Name'])
                else:
                    pass
        

    @commands.command(hidden=True)
    async def baladd(self, ctx: Context, bal:int):
       
        with open('./dicts/Bal.json', 'r+') as k:
            data = json.load(k)
            await ctx.send(data)
            for key in data:
            
                if "Bal" in data[key]:
                    await ctx.send(key)

                    x = self.bot.get_user(int(key))
                    if not x:
                        pass
                    else:

                        data[key]['Bal'] += bal
                        
                        Json(k, data)
                        await ctx.send(data[key]['Bal'])
                else:
                    pass
    
    @commands.command(hidden=True)
    async def removefile(self, ctx: Context, filed, dicte:str):
    
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
    async def data(self, ctx: Context, file1="", data1="", data2="", int1='False', *, add=""):
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
            embed = disnake.Embed(title="Files", description=", ".join(x), colour=thecolor())
            await ctx.send(embed=embed)
            
                
                
                        
    
            
        else:
            if not data1:

                with open(f"./dicts/{file1}.json", 'r+') as k:
                    data = json.load(k)
                    the_num = ''
                    for key in data:
                        
                        if len(key) == len('483631842554019841'):
                            try:

                                the_num = self.bot.get_user(int(key))
                            except:

                                if not the_num:

                                    y.append(f"`{key}` │")
                            else:
                                y.append(f"`{key}: {the_num}` │")
                        else:
                            y.append(f"`{key}`")
                    embed = disnake.Embed(description=", ".join(y))
                    await ctx.send(embed=embed)
                
                
                
                
            else:
                with open(f"./dicts/{file1}.json", 'r+') as k:
                    data = json.load(k)
                    if data1 in data:
                        if not data2:
                            embed = disnake.Embed(description=data[data1])
                            await ctx.send(embed=embed)
                    
                        else:
                            data[data1][data2] = add
                            await ctx.send('yessir')
                            Json(k, data)
                        
                        

                        

                    else:
                        
                            
                        for key in data:
                            y.append(f"`{key}`")
                        embed = disnake.Embed(description=", ".join(y))
                        await ctx.send(embed=embed)
                        
                
    @commands.command(hidden=True, aliases=['save', 'backup'])
    async def savebackup(self, ctx: Context):
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
    async def file(self, ctx: Context, file):
        await ctx.send(file=disnake.File(f"./dicts/{file}"))
    @commands.command(hidden=True)
    async def thecog(self, ctx: Context):
        for thecog in self.bot.cogs:

            cog = self.bot.get_cog(thecog)

            await ctx.send(thecog)

    @commands.command(hidden=True)
    async def formathelp(self, ctx: Context):
        
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
    async def t(self, ctx: Context, d, t=""):
        await thebed(ctx, d, t)

    @commands.command(hidden=True)
    async def addcmd(self, ctx: Context, name, *, cmd):
        with open('./dicts/Commands.json', 'r+') as k:
            data = json.load(k)
            if name in data:
                return await thebed(ctx, 'Already there mate')
            data[name] = {
                'code': cmd,
                'makecmd': f'@bot.command()\nasync def {name}(ctx):'

            }
            Json(k, data)
            thecmd = f"{data[name]['makecmd']}\n    {data[name]['code']}"
            await thebed(ctx, thecmd)
            self.bot.add_command(thecmd)

    @commands.command(hidden=True)
    async def error_tag(self, ctx: Context, errornum:str=None):
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
    async def resolve(self, ctx: Context, errornum:str=None):
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
        m = await ctx.send(embed=disnake.Embed(title='Error', description=f'''
    **error code** : `{errornum}`
    **author** : `{data[errornum]["author"]}`
    **error** : `{data[errornum]["error"]}`
    **cmd** : `{data[errornum]["command"]}`
    ''', color=thecolor()))
        await m.add_reaction('👍')
        reaction, user = await self.bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author)
        await thebed(ctx, '', 'Done')
        del data[errornum]
        Json(k, data)
        
    @commands.command(hidden=True)
    async def forceError(self, ctx):
        await ctx.ss('e')
        
def setup(bot):
  bot.add_cog(Staff(bot))
