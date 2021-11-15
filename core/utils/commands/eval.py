import discord
from discord.ext import commands

#import InfixParser
import json
import io
import textwrap
import contextlib
from traceback import format_exception

from core.utils.utils import Json, thecolor
from core.Paginator import Paginator 

def clean_code(content:str):
    content = content.strip('')
    content = content.replace("‘", "'").replace('“', '"')
    return content


async def run_eval(ctx, code, **kwargs):
    _eval = kwargs.get('_eval')

    local_variables = {
        "discord": discord,
        "commands": commands, 
        "bot": ctx.bot, 
        "client": ctx.bot,
        "ctx": ctx, 
        "channel": ctx.channel, 
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message

    }

    if code == "reset":

        with open('./dicts/Num.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                data[str(ctx.author.id)]['Score'] = 0
                z = data[str(ctx.author.id)]['Score']
            else:
                data[str(ctx.author.id)] = {
                    "Name": ctx.author.name,
                    "Score": 0

                }
            Json(k, data)
            return await ctx.send('reset')
    else:

        with open('./dicts/Num.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                data[str(ctx.author.id)]['Score'] += 1
                z = data[str(ctx.author.id)]['Score']
            else:
                data[str(ctx.author.id)] = {
                    "Name": ctx.author.name,
                    "Score": 1
                }
            Json(k, data)
    
    code = clean_code(code)
        
    stdout = io.StringIO()

    pref = await ctx.bot.get_prefix(ctx.message)
    message = ctx.message.content[len(pref):]

    if _eval == 'dir':
        code = f"print(dir({code}))"
            
    elif _eval == 'return':
        code = f"return {code}"
    
        
    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}",  local_variables, 
            )
            obj = await local_variables["func"]()
        
            result = f"{stdout.getvalue()}{obj}\n"
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))
        pass
   
    result = result.replace('`', '')
    message = message.replace('`', '')
    if result.replace('\n', '').endswith('None') and result != "None":
        result = result[:-5]
    if len(result) < 2000:
        msg = f"```py\nIn[{z}]: {message}\nOut[{z}]: {result}\n```"
    else:
        y = Paginator(ctx)
        return await y.paginate(content=result, name='Eval')

    return msg