from datetime import datetime, timedelta
import discord

string = ''
last_date: float

async def toString(client: discord.Client,target:str):
    global string,last_date
    channel = client.get_channel(1022166337734324236)
    async for msg in channel.history(limit=10):
      if msg.author.id == 375805687529209857:
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
        break

async def remindForMessage(client: discord.Client,message: discord.message.Message,target:str):
  await toString(client,target)
  if last_date > 9 and last_date% 2 == 0:
    channel = client.get_channel(message.channel.id)
    await channel.send(string)
    return

async def remindForInteraction(client: discord.Client,interaction: discord.Interaction,target:str):
  await toString(client,target)
  await interaction.response.send_message(string)
  return
