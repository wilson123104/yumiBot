import json
from typing import Optional
import discord
import sys
sys.path.append("..")
from db import dbConn
import random
from function import dcInfoCommands,getTime
from data import data
from datetime import datetime, timedelta

options = []
thisType_ = ''
class drawLotsHK(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)

    def getData():
        global options
        dataCount = {}
        for x in range(0,100):
            data = dbConn.selectToJson('hkstick','drawLotsHK',f'where id = {x+1}')
            for key in data.keys():
                if key in dataCount:
                    dataCount[key] += 1
                else:
                    dataCount[key] = 1

        for x in range(0,100):
            data = dbConn.selectToJson('luckeyes','drawLotsHK',f'where id = {x+1}')
            for key in data.keys():
                if key in dataCount:
                    dataCount[key] += 1
                else:
                    dataCount[key] = 1
        
        for key in dataCount.keys():
            options.append(discord.SelectOption(label=key))

    if len(data.options) == 0:
        getData()

    @discord.ui.select(options=options, placeholder='請選擇求問之事')
    async def draw(self, interaction: discord.Interaction, select: discord.ui.Select):
        userData = dbConn.select("drawLotsHK_last","user",f'where id={interaction.user.id}')
        print(select.values[0])
        if len(userData) == 0:
            await interaction.response.edit_message(content=f"求{select.values[0]}:\n求籤前先合手，默念「大仙大仙，指點迷津」並說出求籤內容:\n1.中文全名\n2.信男/女\n3.虛齡歲數\n4.稟報求問之事", view=drawLotsHKButtom(type_=select.values[0]))
        else:
            userData = json.loads(userData[0][0].replace("'",'"'))
            if select.values[0] in userData:
                time_2 = getTime.getNowTime().strftime("%Y-%m-%d")
                time_1_struct = datetime.strptime(
                userData[select.values[0]]["time"], "%Y-%m-%d")
                time_2_struct = datetime.strptime(time_2, "%Y-%m-%d")
                # + timedelta(hours=8)
                total_seconds = (time_2_struct - time_1_struct).total_seconds()
                last_date = int(total_seconds / 60 / 60 / 24)
                if last_date <= 7:
                    await interaction.response.edit_message(content=f"求{select.values[0]}:\n聽說同一問題重複求會不準，所以一星期內同一條問題只能問一次喔！", view=drawLotsHKButtomShow(type_=select.values[0]))
                else:
                    await interaction.response.edit_message(content=f"求{select.values[0]}:\n求籤前先合手，默念「大仙大仙，指點迷津」並說出求籤內容:\n1.中文全名\n2.信男/女\n3.虛齡歲數\n4.稟報求問之事", view=drawLotsHKButtom(type_=select.values[0]))
            else:
                await interaction.response.edit_message(content=f"求{select.values[0]}:\n求籤前先合手，默念「大仙大仙，指點迷津」並說出求籤內容:\n1.中文全名\n2.信男/女\n3.虛齡歲數\n4.稟報求問之事", view=drawLotsHKButtom(type_=select.values[0]))

class drawLotsHKButtom(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180,type_):
        global thisType_
        thisType_ = type_
        super().__init__(timeout=timeout)

    @discord.ui.button(label='開始抽籤', style=discord.ButtonStyle.primary)
    async def draw(self, interaction: discord.Interaction, button: discord.ui.Button):
        rNumber = random.randint(1,100)
        embed = getDrawStr(rNumber)
        self.clear_items()
        
        userData = dbConn.select("drawLotsHK_last","user",f'where id={interaction.user.id}')
        if len(userData) == 0:
            newJson = {
                thisType_ :{"number":rNumber, "time":getTime.getNowTime().strftime("%Y-%m-%d")}
            }
            dbConn.insert("user",f'{interaction.user.id},"{str(interaction.user)}","{newJson}"')
        else:
            userData = json.loads(userData[0][0].replace("'",'"'))
            if thisType_ in userData:
                userData[thisType_]["number"] = rNumber
                userData[thisType_]["time"] = getTime.getNowTime().strftime("%Y-%m-%d")
                dbConn.update('user',f'drawLotsHK_last = "{userData}"',f'id = {interaction.user.id}')
            else:
                userData[thisType_] = {"number":rNumber, "time":getTime.getNowTime().strftime("%Y-%m-%d")}
                dbConn.update('user',f'drawLotsHK_last = "{userData}"',f'id = {interaction.user.id}')

        await interaction.response.edit_message(content='求'+thisType_+"\n來源:\nhttps://andy.hk/divine/wongtaisin\nhttps://www.luckeyes.com/celestial/", embed=embed,view=self)
    
    @discord.ui.button(label='返回選擇', style=discord.ButtonStyle.primary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message( content='',view=drawLotsHK())
    
class drawLotsHKButtomShow(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180,type_):
        global thisType_
        thisType_ = type_
        super().__init__(timeout=timeout)

    @discord.ui.button(label='查看上一次的結果', style=discord.ButtonStyle.primary)
    async def showLast(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        userData = dbConn.select("drawLotsHK_last","user",f'where id={interaction.user.id}')
        userData = json.loads(userData[0][0].replace("'",'"'))
        embed = getDrawStr(userData[thisType_]["number"])
        await interaction.response.edit_message(content='求'+thisType_+"\n來源:\nhttps://andy.hk/divine/wongtaisin\nhttps://www.luckeyes.com/celestial/", embed=embed,view=self)
    

def getDrawStr(rNumber:int):
    data = dbConn.select('d.id, d.name, d.poetry, d.content, d.explain, t.name , d.hkstick, d.luckeyes','drawLotsHK d, drawLotsHK_type t',f'WHERE d.id = {rNumber} and d.drawLotsHK_type_id = t.id')
    hkstick = data[0][6].replace("'",'"')
    luckeyes = data[0][7].replace("'",'"')
    hkstick = json.loads(hkstick)
    luckeyes = json.loads(luckeyes)
    str_ = ''

    if thisType_ in hkstick and thisType_ in luckeyes :
        if hkstick[thisType_] in luckeyes[thisType_]:
            str_ = luckeyes[thisType_]
        else:
            str_ = hkstick[thisType_]+"。\n"+luckeyes[thisType_]
    elif thisType_ in hkstick:
        str_ = hkstick[thisType_]+'。'
    elif thisType_ in luckeyes:
        str_ = luckeyes[thisType_]
        
    dataJson = {
        '仙機：':data[0][3],
        '解說及記載：':data[0][4],
        thisType_+"：" : str_
    }
    content = f'第{rNumber}籤\n{data[0][5]}--{data[0][1]}:\n{data[0][2]}'
    embed = dcInfoCommands.dcInfoCommands('',content,0x000ff,dataJson,False,'')
    return embed