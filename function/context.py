import discord
import sys
import variable
sys.path.append("..")
from db import dbConn

async def getContextText(interaction: discord.Interaction,user:discord.Member):
    client = variable.client
    textChannel = variable.textChannel
    selectUser = dbConn.selectUserById(user.id)
    channel = client.get_channel(int(textChannel))
    name = ""
    if user.nick == None:
        name = user.name
    else:
        name = user.nick
    if interaction.channel_id == int(textChannel):
        if len(selectUser) != 0:
            if selectUser[0][4] != 0:
                await interaction.response.send_message(f"{name}從2023年1月3日到現在已經講過{selectUser[0][4]}句話。")
            else:
                await interaction.response.send_message(f"{name}從2023年1月3日到現在沒有講過話。")
        else:
            await interaction.response.send_message(f"{name}從2023年1月3日到現在沒有講過話。")
    else:
        await interaction.response.send_message(f"請在{channel.name}頻道使用這指令",ephemeral=True)