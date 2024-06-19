# imports
import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values
import discord
from discord import Intents, Client, Message
load_dotenv()

#Google Gemini Setup
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

#Discord Bot functionality
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user:
            return
        response = model.generate_content(message.content)
        print(f'Message from {message.author}: {message.content}')
        channel = message.channel
        await channel.send(response.text)

    async def shutdown(ctx):
        await ctx.bot.logout()

#Discord Bot Set up

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.getenv("BOT_TOKEN"))

#bot int permissions 1166571166234944



