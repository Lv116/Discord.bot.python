import random
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
import asyncio
import time
import json
from tinydb import TinyDB, Query, where
import math
import wolframalpha
import wikipedia
import requests
timelast=0
timecheck=0
path_db='/Users/vyom/Desktop/Archives/BotUI/users.json'


token = 'NjI3NzcyOTg1ODcyMjIwMTYx.XZBjOw.A8ysjXiKZpyKAHldN0iZCod3n6g'
bot = commands.Bot(command_prefix = 'qq ' , case_insensitive=True)
bot.remove_command('help')
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

@bot.event
@asyncio.coroutine
async def on_ready():
    change_status.start()
    print("Processing.....")
    print("|||||||||||||||")
    print("Bot has Successfully logged onto Discord...")
    print('Successfully logged in as {0.user}...'.format(bot))
    

@tasks.loop(seconds=600)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status))) 

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.....')

    await update_data(member)



@bot.event
async def on_message(message):
    if message.author==bot.user:
        return
    elif(message.author.bot):
        return
    else:
        global timelast
        await update_data(message.author)
        timlst = timelast
        if time.time() - timlst > 25:
            await add_experience(message,message.author,  10)
            timelast = time.time()

        if message.content.startswith('owo'):
            await message.channel.send('uwu')
        elif message.content.startswith('hi' or 'hey'):
            await message.channel.send('hi there!👋')
        elif 'I need a hug' in message.content:
            await message.channel.send('Awwww._Hugs_🤗')
        elif 'prefix' in message.content:
            await message.channel.send("The prefix of your most loved and the loneliest bot in the world, Tear Drops:tm: is - 'qq '\n\
Cuz you know- Less qq more pew pew. Don't worry feel free to qq all you want around me.")
        elif 'more roles' in message.content:
            await message.channel.send('Make more roles. Gimme more roles......plz')
        elif 'luke' in message.content:
            a=[0,0,0,0,0,1]
            if random.choice(a)==1:
                await message.channel.send('Ban Luke smh...')
        elif 'rigin' in message.content:
            await message.channel.send('UwU, where is rigin-san?')
        elif 'bitch' in message.content:
            await message.author.send('**BITCH**')
        elif 'tears' in message.content:
            await message.channel.send('😭')
        elif 'snoss' in message.content:
            await message.channel.send('_mhm_, snossy snossage')
        elif 'merc' in message.content or 'merctato' in message.content:
            await message.channel.send('https://cdn.discordapp.com/attachments/627146623876857866/627178241920073738/unknown.png')
        elif 'Tear Drops' in message.content:
            await message.channel.send('Yo what up? You talking about me?')
        elif 'poetry' in message.content:
            await message.channel.send('Ooooooh. I wanna hear some _Poetry_....')



    await bot.process_commands(message)



async def update_data(user):
     db = TinyDB(path_db)
     usr=Query()
     if not db.contains(usr['ids']==user.id):
         db.insert({'ids':user.id,'experience': 0, 'level': 1, 'credits': 0,'daily' :0,'hourly':0,'rep':0,'reptime':0})

async def add_experience(message,user, exp):
    db = TinyDB(path_db)
    usr=Query()
    docs = db.search(usr['ids'] == user.id)

    try:
        for doc in docs:
            doc['experience']+=exp
        db.write_back(docs)
    except:
        return
    
    await level_up(message.author, message.channel)


async def level_up(user, channel):
    db = TinyDB(path_db)
    usr=Query()
    docs = db.search(usr['ids'] == user.id)
    for doc in docs:
        lvl_start = doc['level']
        experience = doc['experience']
    x=0
    cnt=0
    while(x<experience):
        cnt+=1
        x=(x*2)+10
    if (experience == x):
        lvl_end = cnt
    else:
        lvl_end = lvl_start
    

    if lvl_start < lvl_end:
        for doc in docs:
            doc['level'] = lvl_end
        db.write_back(docs)
        db = TinyDB(path_db)
        usr=Query()
        docs = db.search(usr['ids'] == user.id)
        ls=lvl_end*150
        for doc in docs:
            doc['credits']+=ls
        db.write_back(docs)
        embed=discord.Embed(title=f'{user} has leveled up to {lvl_end}.',description = f'You have been given {ls} tears for your active-ness.\n\
Saving {ls} tears in your vault of tears.',color = discord.Color.teal()) 
        embed.set_footer(text = '😭')
        await channel.send(embed = embed)        

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server......')
  



@bot.command()
async def ping(ctx):
    phrase=['I am alive...',
            'I was definitely not sleeping...',
            'I was definitely not laughing...',
            'I am still here',
            'You are using a ping command? Why?',
            'You disturbed me. I was crying man....',
            'At your service.']
    ph=random.choice(phrase)
    lsm=round((bot.latency)*100)
    embed=discord.Embed(title='**pong...!**',description = f"_{ph}_ \n**~{lsm} ms taken**......",color = discord.Color.gold()) 
    embed.set_footer(text = '😭')
    await ctx.send(embed = embed)


@bot.command()
async def goaway(ctx):
    await ctx.send('```Ok, then.:cry:I\'mma go...:cry:')
    await logout()

@bot.command()
async def level(ctx):
    user=ctx.message.author
    db = TinyDB(path_db)
    usr=Query()
    docs = db.search(usr['ids'] == user.id)
    for doc in docs:
        lvl = doc['level']
        xp = doc['experience']
    embed= discord.Embed(title=f'Server level card for:',description=f"**{user}**",colour=discord.Color.blurple())
    embed.add_field(name='Level-',value = lvl,inline=False)
    embed.add_field(name='Experience-',value = xp,inline=False)
    embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
    await ctx.send(embed = embed)

@bot.command()
async def profile(ctx, member:discord.Member = None):
    await update_data(member)
    if member==None:
        user=ctx.message.author
    else:
        user=member
    db= TinyDB(path_db)
    usr= Query()
    docs=db.search(usr['ids'] == user.id)
    for doc in docs:
        lvl = doc['level']
        rep = doc['rep']
        xps = doc['experience']
        trs = doc['credits']
        hrs = doc['daily']
    embed= discord.Embed(title='Server Profile card for:',description=f"**{user}**",colour=discord.Color.blurple())
    embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
    embed.add_field(name='**Level**-',value =lvl,inline=False)
    embed.add_field(name='**Experience-**',value =xps,inline=False)
    embed.add_field(name='**Tears-**',value =trs,inline=False)
    embed.add_field(name='**Reputation points**',value = rep,inline=False)
    embed.add_field(name='*Hours remaining in daily cry:*',value=f'{round((86400 - time.time()+hrs)//3600)}',inline=False)
    await ctx.send(embed = embed)



@bot.command(aliases=['command','commands','list'])
async def cmds(ctx):
    embed=discord.Embed(title='**COMMANDS**',description="Here's a list of commands along with functions....",color=discord.Color.green())
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
    

@bot.command(aliases= ['help','helpme'])
async def helps(ctx):  
    embed= discord.Embed(title='**Help....**',description="The prefix for the bot is ' _ '. Yah it's an underscore...",colour=discord.Color.purple())
    embed.set_footer(text= 'For full list of commands with complete functions do _cmds')
    embed.add_field(name='Core',value='ping, help, cmds, botinfo')
    embed.add_field(name='Economy',value='cry, vaultoftears, tear shop',inline=False)
    embed.add_field(name='Entertainment',value='roast, flirt, compliment, geek, nerdystuff, quote, fortune, 8ball, coffee, wannagrabacoffee, book, dadjoke',inline=False)
    embed.add_field(name='Utility',value='purge, ban, kick, unban',inline=False)
    embed.add_field(name='Games',value='diceroll, guessing_game',inline=False)
    await ctx.send(embed = embed)

@bot.command(aliases=['botwhat'])
async def botinfo(ctx):
    embed=discord.Embed(title='**Tear Drops:tm:**',description='A dynamic bot for _crying_, entertainment, economy and _other_ purposes...\n\
This has been coded in Python with the rewrite branch of the discord.py module.\n\
This Bot has been specially designed for this server.Black Mail Inc.[p-n-s].gaah url not working cuz snoss.Gimme server link...:/\
The prefix for the bot is "qq"\
you earn money(tears) by talking in the server.\
NOTE- Copying and replication of bot for proprietary commercial purposes or distribution of closed sourced versions of this WILL NOT be tolerated.\
This bot is under an Apache License V2.0\
This has been uploaded to GitHub only for educational and referencial purposes',colour=discord.Color.purple())   
    embed.set_footer(text='I Hope that you enjoyed the bot....😭')
    embed.set_image(url='https://cdn.discordapp.com/attachments/582605227081990233/627388598181953548/unknown.png')
    await ctx.send(embed = embed)



#
#Economy system
#


#daily credits command
@bot.command(aliases=['morningtears'])
async def daily(ctx):
    user=ctx.message.author
    db = TinyDB(path_db)
    usr=Query()
    docs = db.search(usr['ids'] == user.id)
    trs=[1000,150,150,200,100,50,250,500,200,200,150,100,69420]
    for doc in docs:
        tim= doc['daily']
    if time.time()-tim > 86400:
        tr= random.choice(trs)

        embed= discord.Embed(title='**Tear Dispenser**',description=f'You cried {tr} tears.\n\
Storing them in the vaults of tears.Spend them wisely...💦\nSpend them wisely...',colour=discord.Color.blue())
        embed.set_footer(text= '😭')
        await ctx.send(embed = embed)
        if tr==69420:
            await ctx.send('Damn, that\'s some epic sad-ness...')
        for doc in docs:
            doc['credits'] += tr
            doc['daily'] = time.time()
        db.write_back(docs)
    else:
        embed= discord.Embed(title='**Tear Dispenser**',description=f"You can't cry rn. Let your eyes hydrate.\n\
Wait for like {round((86400 - time.time()+tim)//3600)} hours or something.",colour=discord.Color.blue())
        embed.set_footer(text= '😭')
        await ctx.send(embed = embed)



#hourly credits command
@bot.command(aliases=['timely','hourly'])
async def cry(ctx):
    user=ctx.message.author
    db = TinyDB(path_db)
    usr=Query()
    docs = db.search(usr['ids'] == user.id)
    trs=[5,5,10,10,10,10,20,25,69,0]
    for doc in docs:
        tim= doc['hourly']
    if time.time()-tim > 3600:
        tr= random.choice(trs)
        if tr>1:
            embed= discord.Embed(title='**Timely Tears**',description=f'You cried {tr} tears.\n\
Storing them in the vaults of tears.Spend them wisely...💦\nSpend them wisely...',colour=discord.Color.blue())
            embed.set_footer(text= '😭')
            await ctx.send(embed = embed)
        else:
            tr2=['You were not sad',
             'You were surprisingly too happy to cry',
             'You cried so much already that the tears are not coming out',
             'You really tried but you could not cry',
             'The tears are not coming out...']
            l=random.choice(tr2)
            embed= discord.Embed(title='**Tear Dispenser**',description=f"You can't cry rn.{l}",colour=discord.Color.blue())
            embed.set_footer(text= '😭')
            embed.add_field(name=f'Try again after like an hour.',value='oof',inline=False)
            await ctx.send(embed = embed)

        for doc in docs:
            doc['credits'] += tr
            doc['hourly'] = time.time()
        db.write_back(docs)
    else:
        embed= discord.Embed(title='**Tear Dispenser**',description=f"You can't cry rn. Let your eyes hydrate.\n\
Wait for like {round((3600 - time.time()+tim)//60)} minutes or something.",colour=discord.Color.blue())
        embed.set_footer(text= '😭')
        await ctx.send(embed = embed)




#balance command
@bot.command(aliases=['vaultoftears','tearvault','bal','cur'])
async def vault(ctx):
    user=ctx.message.author
    db= TinyDB(path_db)
    usr= Query()
    docs=db.search(usr['ids'] == user.id)
    for doc in docs:
        trp = doc['credits']
    embed= discord.Embed(title='**Vault of Tears**',description=f"Opening {user}'s vault-of-tears....",colour=discord.Color.blurple())
    embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
    embed.add_field(name=f'Tears',value = trp)
    await ctx.send(embed = embed)




@bot.command(aliases=['addrep'])
async def rep(ctx, member:discord.Member):
    user=ctx.message.author
    if member in ctx.message.guild.members:
        await update_data(member)
        user2=member.id
        if user.id!=user2:
            db = TinyDB(path_db)
            usr=Query()
            docs = db.search(usr['ids'] == user.id)
            for doc in docs:
                tim= doc['reptime']
            if time.time()-tim>3600:
                for doc in docs:
                    doc['reptime'] = time.time()
                db.write_back(docs)
                embed= discord.Embed(title='**Successful**',description=f'{user} has successfully repped {member.mention}\n⬆️',colour=discord.Color.green())
                embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
                await ctx.send(embed = embed)

                db = TinyDB(path_db)
                usr=Query()
                docs2 = db.search(usr['ids'] == user2)
                for do in docs2:
                    do['rep'] += 1
                db.write_back(docs2)
            else:
                embed= discord.Embed(title='**Unsuccessful!!!**',description=f"You can't rep rn.\n\
Wait for like {round((3600 - time.time()+tim)//60)} minutes or something.",colour=discord.Color.red())
                embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
                await ctx.send(embed = embed)
        else:
            embed= discord.Embed(title='**Unsuccessful!!!**',description='You can\'t rep yourself, ya dummy...',colour=discord.Color.red())
            embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
            await ctx.send(embed = embed)


    else:
        embed= discord.Embed(title='**Unsuccessful!!!**',description='Mention someone that exists, ya dummy...',colour=discord.Color.red())
        embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
        await ctx.send(embed = embed)





#credits-transfer command
@bot.command(aliases=['give','share', 'send'])
async def transfer(ctx, amount, member:discord.Member):
    user=ctx.message.author
    if amount.isdigit():
        amount=int(amount)
    if amount=='all':
        db= TinyDB(path_db)
        usr= Query()
        docs=db.search(usr['ids'] == user.id)
        for doc in docs:
            trp = doc['credits']
        amount=trp
    if member in ctx.message.guild.members:
        await update_data(member)
        user2=member.id
        db= TinyDB(path_db)
        usr= Query()
        docs=db.search(usr['ids'] == user.id)
        for i in docs:
            bal = i['credits']
        if bal>amount:
            for doc in docs:   
                doc['credits'] -= amount
            db.write_back(docs)
            db= TinyDB(path_db)
            usr= Query()
            docs2=db.search(usr['ids'] == user2)
            for doc2 in docs2:
                doc2['credits']+= amount
            db.write_back(docs2)
            embed= discord.Embed(title='**Succesful Transaction!!!**',description=f'{amount} tears have been transferred to {member}...',colour=discord.Color.blurple())
            embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
            await ctx.send(embed = embed)

        else:
            embed= discord.Embed(title='**Unsuccesful Transaction!!!**',description='Insufficient tears. Cry more,,,,,:/',colour=discord.Color.blurple())
            embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
            await ctx.send(embed = embed)

    else:
        embed= discord.Embed(title='**Unsuccesful Transaction!!!**',description='Mention someone that exists, ya dummy...',colour=discord.Color.blurple())
        embed.set_footer(text= 'Cry, cry, let the emotions flow through you...😭')
        await ctx.send(embed = embed)
        
"""
@bot.command(aliases=['market'])
async def shop(ctx):
    items= []
    embed=discord.Embed(title='**TearShops**',description = '',colour=discord.Color.red())
"""




@bot.command(aliases= ['diceroll','roll'])
async def dice(ctx, amount : int):
    num = amount
    if num<=6:
        user=ctx.message.author
        db= TinyDB(path_db)
        usr= Query()
        docs=db.search(usr['ids'] == user.id)
        numtemp= random.randint(1,6)
        if num == numtemp:
            for doc in docs:
                doc['credits']+=50
            embed=discord.Embed(title='Dice-roll...🎲', description=f'The dice rolled a {numtemp}.\nYou have been awarded 50 tears for this...', color = discord.Color.dark_red())
            await ctx.send(embed = embed)
            await add_cred(user,50)
        else:
            embed=discord.Embed(title='Dice-roll...🎲', description=f'The dice rolled a {numtemp}.\n\
Your prediction was wrong. 😖', color = discord.Color.dark_red())
            await ctx.send(embed = embed)

    else:
        embed=discord.Embed(title='Dice-roll...🎲', description='Please enter a valid number argument.\n\
Command Usage-> qq dice <num> (between 1 and 6)', color = discord.Color.dark_red())
        await ctx.send(embed = embed)

async def add_cred(user, amount):
    db= TinyDB(path_db)
    usr= Query()
    docs=db.search(usr['ids'] == user.id)
    for doc in docs:
        doc['credits']+=amount


cnt = 0
@bot.command(aliases=['russian-roulette', 'gunshot'])
async def russian_roulette(ctx):
    global cnt
    cnt+=1
    if cnt==0 or cnt==7:
        bulreload()
    global bul
    buls=next(bul)
    if buls == 1:
        embed=discord.Embed(title='Russian Roulette.🔫', description='All you remember is the pain you felt when the bullet pierced your skull.', color = discord.Color.red())
        await ctx.send(embed = embed)
        bulreload()
    else:
        embed=discord.Embed(title='Russian Roulette.🔫', description='Phew, you are safe. wooohooooo', color = discord.Color.orange())
        await ctx.send(embed= embed)
def bulreload():
    global bul
    cnt=0
    but=[0,0,0,0,0,0]
    but[random.randint(0,5)] = 1
    bul=cycle(but)



#
#FUN
#

@bot.command(pass_context=True)
async def echo(ctx,*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await ctx.send(output)


@bot.command(pass_context=True)
async def say(ctx,*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    user=ctx.message.author
    embed = discord.Embed(title =f'{output}', description = f'~{user}',colour= discord.Color.greyple())
    await ctx.send(embed = embed)

                                                                               
@bot.command(pass_context=True)                                                    
async def urban(ctx,*args):                   
    baseurl = "https://www.urbandictionary.com/define.php?term="
    output = ''                                           
    for word in args:                                        
        output += word                                           
        output += '%20'                                   
    await ctx.send(baseurl + output)  

@bot.command(pass_context=True)                                                    
async def define(ctx,*args):                   
    baseurl = "https://www.merriam-webster.com/dictionary/"
    output = ''                                           
    for word in args:                                        
        output += word                                           
        output += '%20'                                   
    await ctx.send(baseurl + output)  

@bot.command(pass_context=True)
async def wiki(ctx,*args):
    qu=' '.join(list(args))
    searchResults = wikipedia.search(qu)
    if not searchResults:
        embed = discord.Embed(title =f'**{qu}**', description = 'It appears that there is no instance of this in Wikipedia index...',colour= discord.Color.dark_red())
        embed.set_footer(text= 'Powered by Wikipedia...')
        await ctx.send(embed = embed)
    else:
        try:
            page = wikipedia.page(searchResults[0])
            l=0
        except wikipedia.DisambiguationError as err:
            page = wikipedia.page(err.options[0])
            l=err.options
  
        wikiTitle = str(page.title.encode('utf-8'))
        wikiSummary = str(page.summary.encode('utf-8'))
        embed = discord.Embed(title =f'**{wikiTitle[1:]}**', description =str(wikiSummary[1:900])+'...',colour= discord.Color.dark_orange(),url=page.url)
        embed.set_footer(text= 'Powered by Wikipedia...')
        if l!=0:
            s=l[1:10]+['...']
            s=','.join(s)
            embed.add_field(name='Did you mean?:',value=s)
        embed.set_image(url=page.images[0])
        await ctx.send(embed = embed)
        

        
    
##



    

###
#error_handleing
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("Invalid command used..... ")

    
bot.run(token)

