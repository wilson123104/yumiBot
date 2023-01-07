from datetime import datetime, timedelta
from db import dbConn
import discord
import variable
from discord import app_commands
import configload 

last_date: float
getChannel = int(configload.getConfigSetting("Credentials", "GetChannel"))
botId = int(configload.getConfigSetting("Credentials", "BotId"))

@app_commands.guild_only()
class remindCommandGroup(app_commands.Group):
    
    @app_commands.command(name='雨兒開台',description="提醒雨兒開台")
    async def remindOpen(client: discord.Client, interaction: discord.Interaction) -> None:
        await remindForInteraction(variable.client,interaction,variable.target)

    @app_commands.command(name='取代',description="取代原本的提醒句子。")
    @app_commands.describe(句子='例子：{奴才}/{雨兒}你他媽的已經{時間}沒開台了，快點開台。')
    async def replace(self, interaction: discord.Interaction, 句子: str) -> None:
        if len(dbConn.selectUserById(interaction.user.id)) == 0:
            dbConn.insertItem('user','id,name',f'{interaction.user.id},"{str(interaction.user)}"')
        dbConn.update('user',f'remind = "{句子}"',f'id = "{interaction.user.id}"')
        await interaction.response.send_message("取代成功",ephemeral=True)

    @app_commands.command(name='還完取代',description="還完原本的提醒句子")
    async def unreplace(self, interaction: discord.Interaction) -> None:
        if len(dbConn.selectUserById(interaction.user.id)) == 0:
            dbConn.insertItem('user','id,name',f'{interaction.user.id},"{str(interaction.user)}"')
        dbConn.update('user','remind = Null',f'id = "{interaction.user.id}"')
        await interaction.response.send_message("還完成功",ephemeral=True)

    @app_commands.command(name='自定義',description='自定義提醒雨兒開台')
    @app_commands.describe(句子='例子：{奴才}/{雨兒}你他媽的已經{時間}沒開台了，快點開台。')
    async def customizeRemind(self, interaction: discord.Interaction, 句子: str) -> None:
        await interaction.response.send_message(await customizeToString(variable.client,variable.target,句子))

async def toString(client: discord.Client,target:str):
    
    global last_date
    channel = client.get_channel(getChannel)
    async for msg in channel.history(limit=10):
      if msg.author.id == botId:
        time_1 = str(msg.created_at).split(".")[0]
        time_2 = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        time_1_struct = datetime.strptime(
          time_1, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
        time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
        total_seconds = (time_2_struct - time_1_struct).total_seconds()
        last_date = total_seconds / 60 / 60 / 24
        last_hour = (last_date - int(last_date)) * 24
        last_min = (last_hour - int(last_hour)) * 60
        last_seconds = (last_min - int(last_min)) * 60
        string = f'<@{target}> 你已經有 {int(last_date)}天 {int(last_hour)}小時 {int(last_min)}分鐘 {int(last_seconds)}秒沒有直播了，我們都很想你<:imuyoxCry:1030059307196219433>，台主最棒最漂亮了<:imuyoxHeart:1030077220481413120>，求求你開個台吧<:imuyoxWuwu:1030080268104634458>'
        return string

async def customizeToString(client: discord.Client,target:str,string:str):
    global last_date
    channel = client.get_channel(getChannel)
    async for msg in channel.history(limit=10):
      if msg.author.id == botId:
        time_1 = str(msg.created_at).split(".")[0]
        time_2 = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        time_1_struct = datetime.strptime(
          time_1, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
        time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
        total_seconds = (time_2_struct - time_1_struct).total_seconds()
        last_date = total_seconds / 60 / 60 / 24
        last_hour = (last_date - int(last_date)) * 24
        last_min = (last_hour - int(last_hour)) * 60
        last_seconds = (last_min - int(last_min)) * 60
        string = string.replace("{奴才}",f'<@{target}>')
        string = string.replace("{雨兒}",f'<@{target}>')
        string = string.replace("{時間}",f'{int(last_date)}天 {int(last_hour)}小時 {int(last_min)}分鐘 {int(last_seconds)}秒')
        return string


async def remindForInteraction(client: discord.Client,interaction: discord.Interaction,target:str):
  remind = dbConn.select('remind','user',f'where id = "{interaction.user.id}"')
  if len(remind) > 0:
    if remind [0][0] != None and remind [0][0] != '':
      await interaction.response.send_message(await customizeToString(client,target,remind[0][0]))
    else:
      await interaction.response.send_message(await toString(client,target))
  else :
    await interaction.response.send_message(await toString(client,target))

"""
async def remindForMessage(client: discord.Client,message: discord.message.Message,target:str):
  await toString(client,target)
  if last_date > 9 and last_date% 2 == 0:
    channel = client.get_channel(message.channel.id)
    await channel.send(string)
    return
""" 