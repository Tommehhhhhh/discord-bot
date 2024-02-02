import discord
import os
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Discord Bot
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='$', intents=intents)

#YouTube API
youtube_api_key = 'AIzaSyDbvMfsO52uzLfw9flqmDZvHaOxrOAJnpg'
youtube_channel_id = 'UCX6OQ3DkcsbYNE6H8uQQuVA'
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    if not check_youtube.is_running():
        check_youtube.start()

@bot.event
async def on_message(message):
    
    if message.content.startswith('$hello'):
        # Respond with "Hello!" in the same channel
        await message.channel.send('Hello!')
    
    if message.content.startswith('$test'):
        check_youtube.restart()

    await bot.process_commands(message)

@tasks.loop(hours=24)
async def check_youtube():
    latest_video = get_latest_video()
    
    if latest_video:
        channel = bot.get_channel(1202949460683005954)
        jimjim = f"<@470895102710251520>"#r"@spaceman_saturn_"
        await channel.send(f"Hey {jimjim}, have you seen the latest MrBeast video 🤔 Check it out here! ->  {latest_video} 😍")

def get_latest_video():
    request = youtube.search().list(
        part='snippet',
        channelId=youtube_channel_id,
        order='date',
        maxResults=1
    )
    
    response = request.execute()
    
    print(response)
    if 'items' in response:
        video = response['items'][0]
        video_id = video['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url

bot.run(os.getenv('TOKEN'))

