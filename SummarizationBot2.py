from TextSummarizationRanking import textSummarizationUsingRanking

import random
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

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
            pass_context=True)
async def summarize(context, *arg):
    summarizeText = textSummarizationUsingRanking(arg)
    await context.send(summarizeText)

bot.run('#')
