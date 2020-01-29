import random
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
import asyncio
import time
import sys
import json


token = 'NjI3NzcyOTg1ODcyMjIwMTYx.XZBjOw.A8ysjXiKZpyKAHldN0iZCod3n6g'

client = commands.Bot(command_prefix = 'qq ' , case_insensitive=True)
client.remove_command('help')
status = cycle(["qq help | :(",
     "with your heart",
     "in tears",
     "with tears",
     "with ",
     "I'm so sad",
     "with your tears...",
     "with your feelings",
     "with sparkles"
     ])

os.chdir('/Users/vyom/Desktop/BotUI')
@client.event
@asyncio.coroutine
async def on_ready():
    change_status.start()
    print("Processing.....")
    print("|||||||||||||||")
    print("Bot has Successfully logged onto Discord...")
    print('Successfully logged in as {0.user}...'.format(client))


@tasks.loop(seconds=600)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status))) 

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.....')
    with open('userst.json' ,'r') as f:
        users= json.load(f)
    
    jsonFile.seek(0)
    await update_data(users, member)
    
    
    with open('userst.json','w') as f:
        json.dump(users,f)




@client.event
async def on_message(message):   
    with open('userst.json' , 'r') as f:
        users= json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author,  10)
    await level_up(users, message.author, message.channel)


    with open('userst.json','w') as f:
        json.dump(users,f)

    await client.process_commands(message)



async def update_data(users, user):
     if not user.id in users:
         users[user.id] = {}
         users[user.id]['experience'] = 0
         users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience']+= exp


async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start= users[user.id]['level']
    lvl_end= int(experience**(1/4))
    if lvl_start < lvl_end:
        await channel.send('{} has leveled up to {}'.format(user.mention, lvl_end))
        users[user.id]['level']= lvl.end





@client.event
async def on_member_remove(member):
    print(f'{member} has left the server......')
  
@client.command()
async def ping(ctx):
    phrase=["I am alive...",
            "I was definitely not sleeping...",
            "I was definitely not laughing...",
            "I'm still here",
            "You are using a ping command? Why?",
            "You disturbed me. I was crying man....",
            "At your service."]
    ph=random.choice(phrase)
    await ctx.send(f'pong...! {ph}  **{round((client.latency)*100)}ms taken......**')
    
@client.command(aliases=['command','commands','list'])
async def cmds(ctx):
    embed=discord.Embed(title='COMMANDS',description="Here's a list of commands along with functions....",color=discord.Color.green())
    embed.add_field(name='helpme',value='displays the command prefix and a basic list of commands...')
    embed.add_field(name='ping',value='The default check command for checking if bot is working...',inline=False)
    embed.add_field(name='cmds',value='Dislays this message containing detailed list of commands with their functions',inline=False)
    embed.add_field(name='botinfo',value='Displays info on the bot...')
    embed.add_field(name='say',value="Makes the bot say sentences that you want it to say. Alias- 'talk'. Usage- '_say <sentence/word>'")
    embed.add_field(name='roast',value="This is the roast command.Go get 'em. Usage- '_roast <@member>'")
    embed.add_field(name='flirt',value="*wink *wink Wanna hit on someone?. Usage-'_flirt <@member>'")
    embed.add_field(name='compliment',value="Wanna commend and compliment someone?. Usage- '_compliment <@member>'")
    embed.add_field(name='geek',value='Prints geeky statements...Aliases= "pimp,techie"')
    embed.add_field(name='nerdystuff',value='Prints stuff for that one nerd in the chat....')
    embed.add_field(name='quote',value='Get ready for some of the best quotes ever....')
    embed.add_field(name='fortune',value='Wanna know the future? Wanna find where you end up?. Aliases="future"')
    embed.add_field(name='8ball',value='Wanna ask questions from the crystal ball?. Aliases="seer". Usage-"_8ball <Question>"')
    embed.add_field(name='coffee',value='Just try a nice cup of coffee.............')
    embed.add_field(name='wannagrabacoffe',value="Wanna ask your e-crush out? Here you go.... Usage-'_wannagrabacoffee <@member>'")
    embed.add_field(name='book',value='Wanna read a book. Here are some recommendations....')
    embed.add_field(name='dadjoke', value='Wanna hear some cringey bad jokes?')
    embed.add_field(name='diceroll', value='Rolls a dice. If you get a number higher than the bot then you win...')
    embed.add_field(name='guessing_game',value='Bot thinks of a number smaller than 15 and you have to guess that number. If you guess it correct, you win')
    embed.set_footer(text='I hope that helped......')
    await ctx.send(embed=embed)
    

@client.command(aliases= ['help','helpme'])
async def helps(ctx):  
    embed= discord.Embed(title='**Help....**',description="The prefix for the bot is ' _ '. Yah it's an underscore...",colour=discord.Color.purple())
    embed.set_footer(text= 'For full list of commands with complete functions do _cmds')
    embed.add_field(name='Core',value='ping, help, cmds, botinfo')
    embed.add_field(name='Economy',value='cry, vaultoftears, tear shop',inline=False)
    embed.add_field(name='Entertainment',value='roast, flirt, compliment, geek, nerdystuff, quote, fortune, 8ball, coffee, wannagrabacoffee, book, dadjoke',inline=False)
    embed.add_field(name='Utility',value='purge, ban, kick, unban',inline=False)
    embed.add_field(name='Games',value='diceroll, guessing_game',inline=False)
    await ctx.send(embed = embed)
    
@client.command(aliases=['botwhat'])
async def botinfo(ctx):
    embed=discord.Embed(title='Tear Ducts:tm:',description='A dynamic bot for crying, entertainment, economy and other purposes...\n\
This has been coded in Python with the rewrite branch of the discord.py module.\n\
This Bot has been specially designed for this server.Black Mail Inc.[p-n-s].gaah url not working cuz snoss.Gimme server link...:/\
The prefix for the bot is "qq"\
you earn money(tears) by talking in the server.\
NOTE- Copying and replication of bot for proprietary commercial purposes or distribution of closed sourced versions of this WILL NOT be tolerated.\
This bot is under an Apache License V2.0\
This has been uploaded to GitHub only for educational and referencial purposes',color=discord.Color.purple())   
    embed.set_footer(text='I Hope that you enjoyed the bot....:sob:')
    embed.set_image(url='https://cdn.discordapp.com/attachments/582605227081990233/627388598181953548/unknown.png')
    await ctx.send(embed = embed)


@client.command(pass_context=True,aliases=['daily','sob'])
async def cry(ctx):
    tr=[0,100,150,150,200,100,50,250,500,200,1,200,150,100,3000]
    usr=ctx.message.author
    if tr!=0 and tr!=1:
        await ctx.send(f' You cried {random.choice(tr)} tears.\n\
Storing them in the vaults of tears.')
        await ctx.send('💦')
        await ctx.send('Spend them wisely...')
    elif tr!=0:
        await ctx.send(f'You really tried but only 1 tear came out....\n\
Storing it in the vaults of tears.')
        await ctx.send('💧')
        await ctx.send('Spend it wisely...')
    else:
        tr2=['You were not sad',
             'You were surprisingly too happy to cry',
             'You cried so much already that the tears are not coming out',
             'You really tried but you could not cry',
             'The tears are not coming out...']
        await ctx.send(f'{random.choice(tr2)}')


@client.command(pass_context=True)
async def echo(ctx,*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await ctx.send(output)
    
                                                                               
@client.command(pass_context=True)                                                    
async def urban(ctx,*args):                   
    baseurl = "https://www.urbandictionary.com/define.php?term="
    output = ''                                           
    for word in args:                                        
        output += word                                           
        output += '%20'                                   
    await ctx.send(baseurl + output)  

@client.command(pass_context=True)                                                    
async def define(ctx,*args):                   
    baseurl = "https://www.merriam-webster.com/dictionary/"
    output = ''                                           
    for word in args:                                        
        output += word                                           
        output += '%20'                                   
    await ctx.send(baseurl + output)  

#error_handleing
#why the fuck am I not using classes...
@client.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("Invalid command used..... ")
client.run(token)
