import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv


def run_bot():
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='?', intents=intents)

    queues = {}
    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn -filter:a "volume=0.25"'}

    @client.event
    async def on_ready():
        print('Bot is ready.')

    async def play_next(ctx):
        if queues[ctx.guild.id] != {}:
            link = queue[ctx.guild.id].pop(0)
            await play(ctx, link)

    @client.command(name="play")
    async def play(ctx, link):
        try:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
            voice_clients[ctx.guild.id].play(player, after=lambda i: asyncio.run_coroutine_threadsafe(play_next(ctx),
                                                                                                      client.loop))
        except Exception as e:
            print(e)

    @client.command(name="clear")
    async def clear(ctx):
        if ctx.guild.id not in queues:
            queues[ctx.guild.id].clear()
            await ctx.send('Cleared.')
        else:
            await ctx.send('Nothing to clear.')

    @client.command(name="pause")
    async def pause(ctx):
        try:
            voice_clients[ctx.guild.id].pause()
            message = await ctx.channel.send('Paused music')
        except Exception as e:
            print(e)

    @client.command(name="resume")
    async def resume(ctx):
        try:
            voice_clients[ctx.guild.id].resume()
            message = await ctx.channel.send('Resumed music')
        except Exception as e:
            print(e)

    @client.command(name="stop")
    async def stop(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)

    @client.command(name="queue")
    async def queue(ctx, *, url):
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []
        queues[ctx.guild.id].append(url)
        await ctx.send("Added to queue!")

    @client.command(name="skip")
    async def skip(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await play_next(ctx)
            await ctx.send("Skipped current track!")
        except Exception as e:
            print(e)

    client.run(os.getenv("BOT_TOKEN"))
