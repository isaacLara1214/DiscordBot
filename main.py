# This example requires the 'message_content' intent.
import os
from dotenv import load_dotenv, dotenv_values
import discord
from discord import Intents, Client, Message
load_dotenv()


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        channel = message.channel
        await channel.send('bitch')

    async def shutdown(ctx):
        await ctx.bot.logout()

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv("BOT_TOKEN"))
