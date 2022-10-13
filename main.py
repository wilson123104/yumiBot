#導入 Discord.py
import discord
from discord import app_commands 
import configload
from datetime import datetime, timedelta
from function import remind
lastDate = ''
guild_id = configload.getConfigSetting("Credentials", "Guild_id")
token = configload.getConfigSetting("Credentials", "Token")
target = configload.getConfigSetting("Credentials", "TargetUser")

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await bot.sync(guild = discord.Object(id=guild_id)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f'目前登入身份：{client.user}')

client = aclient()
bot = app_commands.CommandTree(client)

#當有訊息時
@client.event
async def on_message(message: discord.message.Message):
  global lastDate
  if message.author == client.user:
    return

  if message.author.id == int(target) and datetime.today().strftime("%Y%m%d") != lastDate:
    lastDate = (datetime.now()+timedelta(hours=8)).strftime("%Y%m%d")
    await remind.remindForMessage(client,message,target)

  if message.content == "--v":
    await message.channel.send("版本 1.0.0")
    return

@bot.command(guild = discord.Object(id=guild_id), name = 'ig', description='雨兒的Ig')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.instagram.com/dear.yumii/") 

@bot.command(guild = discord.Object(id=guild_id), name = 'twitch', description='雨兒的Twitch')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.twitch.tv/imuy_oxo") 

@bot.command(guild = discord.Object(id=guild_id), name = 'remind', description='提醒雨兒開台')
async def slash2(interaction: discord.Interaction):
    await remind.remindForInteraction(client,interaction,target)

client.run(token)