from datetime import datetime, timedelta
import discord

last_date: float

async def toString(client: discord.Client,target:str,string:str):
    global last_date
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
        string = string.replace("{奴才}",f'<@{target}>')
        string = string.replace("{雨兒}",f'<@{target}>')
        string = string.replace("{時間}",f'{int(last_date)}天 {int(last_hour)}小時 {int(last_min)}分鐘 {int(last_seconds)}秒')
        return string

async def remindForInteraction(client: discord.Client,interaction: discord.Interaction,target:str, string:str):
  await interaction.response.send_message(await toString(client,target,string))
  return
