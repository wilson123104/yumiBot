#導入 Discord.py
import discord
from discord import app_commands
import configload 
from function import remind,drawCard,drawLotsHK, posterBoard
from game import truthNoAdventure
import variable

lastDate = ''
guild_id = configload.getConfigSetting("Credentials", "Guild_id")
token = configload.getConfigSetting("Credentials", "Token")
target = configload.getConfigSetting("Credentials", "TargetUser")
drawLotsHK_room_ID = configload.getConfigSetting("Credentials", "DrawLotsHK_room_ID")
drawCard_room_ID = configload.getConfigSetting("Credentials", "DrawCard_room_ID")
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

variable.setClient(client)
variable.setToken(token)
variable.setTarget(target)

#當有訊息時
@client.event
async def on_message(message: discord.message.Message):
  global lastDate
  if message.author == client.user:
    return

  """
  if message.author.id == int(target) and datetime.today().strftime("%Y%m%d") != lastDate:
    lastDate = (datetime.now()+timedelta(hours=8)).strftime("%Y%m%d")
    await remind.remindForMessage(client,message,target)
  """
  if message.content == "--v":
    await message.channel.send("版本 1.0.0")
    return
  
bot.add_command(remind.remindCommandGroup(name='提醒'),guild= discord.Object(id=guild_id))

@bot.command(guild = discord.Object(id=guild_id), name = 'ig', description='雨兒的Ig')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.instagram.com/dear.yumii/") 

@bot.command(guild = discord.Object(id=guild_id), name = 'twitch', description='雨兒的Twitch')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.twitch.tv/imuy_oxo") 

@bot.command(guild = discord.Object(id=guild_id), name = '抽卡', description='無聊抽卡，聽說雨兒會考慮給獎勵')
async def slash2(interaction: discord.Interaction):
    if interaction.channel_id == int(drawCard_room_ID):
        await interaction.response.send_message(embed=drawCard.drawCard(client))

@bot.command(guild = discord.Object(id=guild_id), name = '黃大仙求籤', description='香港的黃大仙求籤')
async def slash2(interaction: discord.Interaction):
    if interaction.channel_id == int(drawLotsHK_room_ID):
        await interaction.response.send_message(view=drawLotsHK.drawLotsHK())

bot.add_command(posterBoard.posterBoardCommandGroup(name='貼堂文'),guild= discord.Object(id=guild_id))

#真心話不冒險
#bot.add_command(truthNoAdventure.TruthNoAdventureCommandGroup(name='真心話不冒險'),guild= discord.Object(id=guild_id))
    
client.run(token)