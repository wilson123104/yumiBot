import discord
import random
import sys
from discord import app_commands
sys.path.append("..")
from function import dcInfoCommands
from db import dbConn

def getPosterBoard():
    datas = dbConn.select("*","posterBoard","")
    index = 1
    array = []
    for data in datas:
        array.append(app_commands.Choice(name=data[1], value=index))
        index += 1
    return array

@app_commands.guild_only()
class posterBoardCommandGroup(app_commands.Group):
    dcPosterBoardArray = getPosterBoard()
    @app_commands.command(name='文章',description="所有貼堂的文章")
    @app_commands.describe(文章選擇='文章選擇')
    @app_commands.choices(文章選擇=dcPosterBoardArray)
    async def dcPosterBoard(self, interaction: discord.Interaction,文章選擇: app_commands.Choice[int]) -> None:
        datas = dbConn.select("*","posterBoard",f"where id = '{文章選擇.value}'")
        userData = {
            "內文:":datas[0][3]
        }
        await interaction.response.send_message(embed=dcInfoCommands.dcInfoCommands("", "題目: "+datas[0][1]+"          作者: "+datas[0][2], 0x000ff, userData, True, ""))