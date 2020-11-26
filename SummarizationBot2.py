from TextSummarizationRanking import textSummarizationUsingRanking

import os
import random
import urllib.request
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command(name='read-context',
            aliases=['message', 'msg'],
            pass_context=True)
async def readMessage(context):
    await context.send(context.message)

@bot.command(name='hello',
            description="Just saying hi.",
            brief="Hello from me the bot.",
            aliases=['hi', 'sup'],
            pass_context=True)
async def hello(context):
    possible_responses = [
        "Hello to you too!",
        "What a fine day isn't it",
        "Yo, what sup",
        "Quite intresting way to say"
    ]
    await context.send( random.choice(possible_responses) + ", "
                + context.message.author.mention)

@bot.command(name='summarize',
            description="Summarize a text that you give.",
            brief="Call this function with the text you want to summarize",
            aliases=['summarize-text', 'sum-text', 'sum-txt'],
            pass_context=True)
async def summarize(context, *arg):
    summarizeText = textSummarizationUsingRanking(arg)
    await context.send(summarizeText)

def readFile(url):
    # First download the file
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0')
    filename, headers = opener.retrieve(url, 'downloads/temp.txt')
    # Read the file and split it
    split_text = []
    with open(filename) as f:
        for line in f:
            split_text.extend( line.replace('  ', ' ').split(' ') )
    print(split_text)
    # After that remove the file
    os.remove(filename)
    return split_text

@bot.command(name='summarizeFile', 
            description="Summarize from the first file you attach.", 
            brief="Call this function and don't forget to attach a txt file",
            aliases=['sum-file', 'summarize-file', 'sumFile'],
            pass_context=True)
async def summarizeFile(context, *arg):
    # Get the attachments url
    attch_url = context.message.attachments[0].url
    # If the url ends with .txt that means the file type is text
    if attch_url.endswith('.txt'):
        # Get the attachment file
        splitted_text = readFile(attch_url)
        # Summarize the text
        summarizeText = textSummarizationUsingRanking(splitted_text)
        await context.send(summarizeText)
    else:
        possible_responses = [
            "The file is not in .txt format.",
            "Well, I can't read non-txt format file",
            "Are you teasing me??? (ಠ╭╮ಠ)"
        ]
        await context.send(random.choice(possible_responses) + ", "
                + context.message.author.mention)

bot.run('TOKEN')
