import datetime
from datetime import datetime, time, timezone
import discord
from discord.ext import tasks, commands
import random
import csv
import configparser

# Open our config file and parse into our constants
config = configparser.ConfigParser()
config.read("config.ini")
settings = config['DEFAULT'] # Just used to shorten the following code

BOT_TOKEN = settings['BOT_TOKEN']
CHANNEL_ID = int(settings['CHANNEL_ID'])
ANNOUNCE_TIME = time(hour=int(settings['ANNOUNCE_TIME_HOUR']), minute=int(settings['ANNOUNCE_TIME_MINUTE']))
WEEK_DAY = int(settings['WEEK_DAY'])

# Declare the bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("PixelPolyPromptBot is Ready")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Prompterbot is online")
    loopy.start()

# !idea: add a prompt to the csv
@bot.command()
async def idea(ctx, *, ideaString):
    for c in ideaString: # Check each character
        checkerList = [ c.isalpha(), c.isdecimal(), c.isdigit(), c.isnumeric(), c.isspace() ]
        if any(checkerList) == False:
            await ctx.send(f"I can only take numbers, letters, and spaces, sorry!")
            return
    csvStrings = []
    with open('prompts.csv', 'r', newline='') as csvIn: # Open in read mode
        csvReader = csv.reader(csvIn, delimiter=',')
        try:
            csvStrings = next(csvReader) # Grab just the first row
        except:
            pass # Don't need to do anything with a failure, just prevent error
        for string in csvStrings:
                if ideaString == string:
                    await ctx.send(f"Idea **{ideaString}** was already in the list, try another!")
                    return
    with open('prompts.csv', 'w', newline='') as csvOut: # Open in write mode
        csvStrings.append(f"{ideaString}") # If we didn't return early during reading, add the new prompt
        writer = csv.writer(csvOut)
        writer.writerow(csvStrings)
        await ctx.send(f"Idea **{ideaString}** added, thanks!")

# !gimme a random prompt
@bot.command()
async def gimme(ctx):
	await giveme()
	
# !gimmie a random prompt (just an alternate spelling)
@bot.command()
async def gimmie(ctx):
	await giveme()

# !remove a prompt from the csv
@bot.command()
async def remove(ctx, *, ideaString):
    csvStrings = []
    with open('prompts.csv', 'r', newline='') as csvIn:
        csvReader = csv.reader(csvIn, delimiter=',')
        try:
            csvStrings = next(csvReader)
        except:
            pass 
        try:
            csvStrings.remove(ideaString)
        except:
            pass 
    with open('prompts.csv', 'w', newline='') as csvOut:
        writer = csv.writer(csvOut)
        writer.writerow(csvStrings)
    await ctx.send(f"If **{ideaString}** was in the list, it isn't anymore!")

# !reroll the weekly prompt
@bot.command()
async def reroll(ctx):
    await weekly()

# Event timer to run the weekly prompt
@tasks.loop(time = ANNOUNCE_TIME)
async def loopy():
    print("loopy ran")
    if datetime.now(timezone.utc).weekday() == WEEK_DAY: # This was the easiest way to make a weekly task with the Discord stuff
        print("and it was on the right day")
        await weekly()

# Weekly prompt
async def weekly():
    channel = bot.get_channel(CHANNEL_ID)
    csvStrings = []
    with open('prompts.csv', 'r', newline='') as csvIn:
        csvReader = csv.reader(csvIn, delimiter=',')
        try:
            csvStrings = next(csvReader)
        except:
            await channel.send(f"The prompt list is empty! Try adding some more ideas and !reroll.")
            return
    if len(csvStrings) > 0:
        await channel.send(f"Hi Polywigs and Mesh Goblins! This week's prompt is **{random.choice(csvStrings)}**!")
    else:
        await channel.send(f"The prompt list is empty! Try adding some more ideas and !reroll.")

# Giveme command defined as a separate function to allow calling from !gimme or !gimmie spellings
async def giveme():
    channel = bot.get_channel(CHANNEL_ID)
    csvStrings = []
    with open('prompts.csv', 'r', newline='') as csvIn:
        csvReader = csv.reader(csvIn, delimiter=',')
        try:
            csvStrings = next(csvReader)
        except:
            await channel.send(f"The prompt list is empty! Try adding some more ideas first.")
            return
    if len(csvStrings) > 0:
        await channel.send(f"Your prompt is **{random.choice(csvStrings)}**!")
    else:
        await channel.send(f"The prompt list is empty! Try adding some more ideas first.")

bot.run(BOT_TOKEN)
