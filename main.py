#導入 Discord.py
import discord
from discord import app_commands 
import configload
from datetime import datetime, timedelta

target = 303096379696349185
lastDate = ''
guild_id = configload.getConfigSetting("Credentials", "Guild_id")
token = configload.getConfigSetting("Credentials", "Token")
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
  if message.author.id == target and datetime.today().strftime(
      "%Y%m%d") != lastDate:
    channel = client.get_channel(1022166337734324236)
    async for msg in channel.history(limit=10):
      if msg.author.id == 375805687529209857:
        time_1 = str(msg.created_at).split(".")[0]
        time_2 = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        time_1_struct = datetime.strptime(
          time_1, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
        time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S")
        total_seconds = (time_2_struct - time_1_struct).total_seconds()
        last_date = total_seconds / 60 / 60 / 24
        last_hour = (last_date - int(last_date)) * 24
        last_min = (last_hour - int(last_hour)) * 60
        last_seconds = (last_min - int(last_min)) * 60
        channel = client.get_channel(message.channel.id)
        lastDate = datetime.today().strftime("%Y%m%d")
        if last_date > 2:
          await channel.send(
            f'<@{target}> 你已經有 {int(last_date)}天 {int(last_hour)}小時 {int(last_min)}分鐘 {int(last_seconds)}秒沒有直播了，我們都很想你，不如開個台吧!'
          )
          return
        break
  if message.content == "--v":
    await message.channel.send("版本 1.0.0")
    return

@bot.command(guild = discord.Object(id=guild_id), name = 'ig', description='雨兒的Ig')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.instagram.com/dear.yumii/") 

@bot.command(guild = discord.Object(id=guild_id), name = 'twitch', description='雨兒的Twitch')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.twitch.tv/imuy_oxo") 

#多選項
"""
@bot.command(guild = discord.Object(id=guild_id), name = 'tester2', description='testing')
@app_commands.describe(fruits='fruits to choose from')
@app_commands.choices(fruits=[
    app_commands.Choice(name='apple', value=1),
    app_commands.Choice(name='banana', value=2),
    app_commands.Choice(name='cherry', value=3),
])
async def fruit(interaction: discord.Interaction, fruits: app_commands.Choice[int]):
    await interaction.response.send_message(f'Your favourite fruit is {fruits.name}.', ephemeral = True)

"""

client.run(token)
