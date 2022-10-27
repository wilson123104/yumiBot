import random
from typing import  List, Optional
import discord
from discord import CategoryChannel, Member, Message, TextChannel, User, VoiceChannel, app_commands
import sys
sys.path.append("..")
from db import dbConn
from function import dcInfoCommands
class MemberData():
    #state 0=已加入 1=已準備
    def __init__(self,user:User,state:int):
        self.user = user
        self.state = state
        self.answer:bool = None
        self.answerNumber:int = None
        self.score = 0

class RoomData():
    def __init__(self,comminicateChannel: TextChannel,roomowner: User or Member, textChannel: TextChannel, hintMessage:TextChannel, voiceChannel: VoiceChannel,categoryChannel:CategoryChannel,topicOptions:int, roomStart:bool,memberMessage: Message = None,members:List[MemberData] = []):
        self.roomowner = roomowner
        self.textChannel = textChannel
        self.voiceChannel = voiceChannel
        self.categoryChannel = categoryChannel
        self.members = members
        self.memberMessage = memberMessage
        self.hintMessage = hintMessage
        self.topicOptions = topicOptions #0=題庫 1＝自由出
        self.roomStart = roomStart
        self.comminicateChannel = comminicateChannel
        self.question = ''
        self.questionId = None
        self.questionBank = []
        self.answer:bool = None
        self.answerNumber:int = None
        self.score = 0
        
options = []
class QuestionBank(discord.ui.View):
    def __init__(self, room:RoomData, timeout: Optional[float] = 180):
        global options 
        for i in range(0, len(options)):
            options.pop(0)
        for i in range(0, len(room.members)+2):
            options.append(discord.SelectOption(label=f'{i}'))
        super().__init__(timeout=timeout)

    @discord.ui.select(options=options, placeholder='猜人數')
    async def draw(self, interaction: discord.Interaction, select: discord.ui.Select):
        room:RoomData
        if RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getMemberRoom(interaction.user.id).textChannel.id != interaction.channel_id:
            await interaction.response.send_message(f"你去錯房間了，你的房間名稱是 真心話不冒險 : "+RoomDataDef.getMemberRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
        elif not RoomDataDef.isMember(interaction.user.id) and not RoomDataDef.isRoomowner(interaction.user.id):
            await interaction.response.send_message("你沒有加入任何房間",ephemeral=True)
        else:
            if RoomDataDef.isRoomowner(interaction.user.id):
                room = RoomDataDef.getRoomownerRoom(interaction.user.id) 
                room.answerNumber = int(select.values[0])
            else:
                RoomDataDef.getUserData(interaction.user.id).answerNumber = int(select.values[0])
                room = RoomDataDef.getMemberRoom(interaction.user.id)
            await room.hintMessage.edit(content=RoomDataDef.QuestionBankDraw(interaction.channel_id,False,RoomDataDef.AllAnswer(interaction.channel_id)))
            if RoomDataDef.AllAnswer(interaction.channel_id):
                button1 = self.children[3]
                button1.disabled = False
                self.children[0].disabled = True
                self.children[1].disabled = True
                self.children[2].disabled = True
                await interaction.response.edit_message(view=self)
            else:
                await interaction.response.defer(thinking=False)

    @discord.ui.button(label='是', style=discord.ButtonStyle.primary)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        room:RoomData
        if RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getMemberRoom(interaction.user.id).textChannel.id != interaction.channel_id:
            await interaction.response.send_message(f"你去錯房間了，你的房間名稱是 真心話不冒險 : "+RoomDataDef.getMemberRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
        elif not RoomDataDef.isMember(interaction.user.id) and not RoomDataDef.isRoomowner(interaction.user.id):
            await interaction.response.send_message("你沒有加入任何房間",ephemeral=True)
        else:
            if RoomDataDef.isRoomowner(interaction.user.id):
                room = RoomDataDef.getRoomownerRoom(interaction.user.id) 
                room.answer = True
            else:
                RoomDataDef.getUserData(interaction.user.id).answer = True
                room = RoomDataDef.getMemberRoom(interaction.user.id)
            await room.hintMessage.edit(content=RoomDataDef.QuestionBankDraw(interaction.channel_id,False,RoomDataDef.AllAnswer(interaction.channel_id)))
            if RoomDataDef.AllAnswer(interaction.channel_id):
                button1 = self.children[3]
                button1.disabled = False
                self.children[0].disabled = True
                self.children[1].disabled = True
                self.children[2].disabled = True
                await interaction.response.edit_message(view=self)
            else:
                await interaction.response.defer(thinking=False)
    
    @discord.ui.button(label='否', style=discord.ButtonStyle.primary)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        room:RoomData
        if RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getMemberRoom(interaction.user.id).textChannel.id != interaction.channel_id:
            await interaction.response.send_message(f"你去錯房間了，你的房間名稱是 真心話不冒險 : "+RoomDataDef.getMemberRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
        elif not RoomDataDef.isMember(interaction.user.id) and not RoomDataDef.isRoomowner(interaction.user.id):
            await interaction.response.send_message("你沒有加入任何房間",ephemeral=True)
        else:
            if RoomDataDef.isRoomowner(interaction.user.id):
                room = RoomDataDef.getRoomownerRoom(interaction.user.id) 
                room.answer = False
            else:
                RoomDataDef.getUserData(interaction.user.id).answer = False
                room = RoomDataDef.getMemberRoom(interaction.user.id)
            await room.hintMessage.edit(content=RoomDataDef.QuestionBankDraw(interaction.channel_id,False,RoomDataDef.AllAnswer(interaction.channel_id)))
            if RoomDataDef.AllAnswer(interaction.channel_id):
                button1 = self.children[3]
                button1.disabled = False
                self.children[0].disabled = True
                self.children[1].disabled = True
                self.children[2].disabled = True
                await interaction.response.edit_message(view=self)
            else:
                await interaction.response.defer(thinking=False)

    @discord.ui.button(label='下一條', style=discord.ButtonStyle.primary, disabled=True)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if RoomDataDef.isRoomowner(interaction.user.id):
            RoomDataDef.resetAll(interaction.channel_id)
            await RoomDataDef.getRoomDataByTextChannelId(interaction.channel_id).hintMessage.edit(content=RoomDataDef.QuestionBankDraw(interaction.channel_id,True,False))
            button1 = self.children[3]
            button1.disabled = True
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[2].disabled = False
            await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message("你不是房主",ephemeral=True)


class RoomDataDef():
    def resetAll(textChannelId):
        channel = RoomDataDef.getRoomDataByTextChannelId(textChannelId)
        for member in channel.members:
            member.answer = None
            member.answerNumber = None
        channel.answer = None
        channel.answerNumber = None

    def isRoomowner(roomownerId)->bool:
        isRoomowner = False
        roomData:RoomData
        for room in rooms:
            roomData = room[list(room.keys())[0]]
            if roomData.roomowner.id == roomownerId:
                isRoomowner = True
                break
        return isRoomowner

    def isMember(memberId)->bool:
        roomData:RoomData
        for room in rooms:
            roomData = room[list(room.keys())[0]]
            for member in roomData.members:
                if member.user.id == memberId:
                    return True
        return False

    def getRoomownerRoom(roomownerId)->RoomData:
        roomData:RoomData
        for room in rooms:
            roomData = room[list(room.keys())[0]]
            if roomData.roomowner.id == roomownerId:
                return roomData
        return None

    def getMemberRoom(memberId)->RoomData:
        roomData:RoomData
        for room in rooms:
            roomData = room[list(room.keys())[0]]
            for member in roomData.members:
                if member.user.id == memberId:
                    return roomData
        return None
    
    def getUserData(user)->MemberData:
        roomData:RoomData
        for room in rooms:
            roomData = room[list(room.keys())[0]]
            for member in roomData.members:
                if member.user.id == user:
                    return member
        return None

    def getRoomDataByRoomownerId(roomownerId)->RoomData:
        roomData:RoomData
        for room in rooms:
            roomData = room[list(room.keys())[0]]
            if roomData.roomowner.id == roomownerId:
                return roomData
        return None

    def isOnPlayRoom(textChannelId)->bool:
        isRoomowner = False
        for room in rooms:
            roomData:RoomData = room[list(room.keys())[0]]
            if roomData.textChannel.id == textChannelId:
                isRoomowner = True
                break
        return isRoomowner

    def getRoomDataByTextChannelId(textChannelId)->RoomData:
        for room in rooms:
            roomData:RoomData = room[list(room.keys())[0]]
            if roomData.textChannel.id == textChannelId:
                return roomData
        return None

    def getAllMemberMessageByRoomowner(textChannelId)->str:
        roomData = RoomDataDef.getRoomDataByTextChannelId(textChannelId)
        members = ''
        
        if len(roomData.members) == 0:
            members = '沒有'
        else:
            for member in roomData.members:
                state:str = ''
                if member.state == 0:
                    state = "未準備"
                elif member.state == 1:
                    state = "已準備"
                members += f'<@{member.user.id}> : {state}, '

        if len(roomData.members) == 0:
            return (f"房主:<@{roomData.roomowner.id}>\n成員:"+members)
        else:
            return (f"房主:<@{roomData.roomowner.id}>\n成員:"+members)[:-2]

    def isStart(textChannelId)->bool:
        for room in rooms:
            roomData:RoomData = room[list(room.keys())[0]]
            if roomData.textChannel.id == textChannelId:
                return roomData.roomStart
            
    def isAllReady(textChannelId)->bool:
        for room in rooms:
            roomData:RoomData = room[list(room.keys())[0]]
            if roomData.textChannel.id == textChannelId:
                for member in roomData.members:
                    if member.state == 0:
                        return False
        return True
    
    def outRoom(memberId) -> None:
        roomData:RoomData
        for room in rooms:
            roomData = room[list(room.keys())[0]]
            for index, member in enumerate(roomData.members):
                if member.user.id == memberId:
                    roomData.members.pop(index)

    def getQuestionInDb(textChannelId):
        channel = RoomDataDef.getRoomDataByTextChannelId(textChannelId)
        channel.questionBank = dbConn.select("question,id","truthNoAdventure","")
        

    def QuestionBankDraw(textChannelId, isDraw, isShow) -> str:
        channel = RoomDataDef.getRoomDataByTextChannelId(textChannelId)

        if isDraw and len(channel.questionBank) == 0:
            winArray = []
            upNumber = channel.score
            winer = ''
            
            for member in channel.members:
                if member.score > upNumber:
                    upNumber = member.score
                
            if channel.score == upNumber:
                winArray.append(f'<@{channel.roomowner.id}>')
            
            for member in channel.members:
                if member.score == upNumber:
                    winArray.append(f'<@{member.user.id}>')
            
            for win in winArray:
                winer += win+", "

            if upNumber != 0:
                return (f"沒題目了\n\n勝出者:{winer[:-2]}\n\n分數:{upNumber}\n\n你是贏了，可是沒獎勵")
            else:
                return (f"沒題目了\n\n勝出者:{winer[:-2]}\n\n分數:{upNumber}\n\n都0分,呵呵快去了解大家一下")
            
        else:
            question = ''
            members = ''
            if isDraw:
                print(len(channel.questionBank)-1)
                rNumber = random.randint(0,len(channel.questionBank)-1)
                question = channel.questionBank[rNumber][0]
                channel.questionId = channel.questionBank[rNumber][1]
                channel.questionBank.pop(rNumber)
                channel.question = question
            else:
                question = channel.question

            if isShow:
                
                data = dbConn.select("*","truthNoAdventureAnswer",f"where userId == '{channel.roomowner.id}' and truthNoAdventure_id == '{channel.questionId}'")
                count = 0
                if len(dbConn.selectUserById(channel.roomowner.id)) == 0:
                    dbConn.insertItem('user','id,name',f'{channel.roomowner.id},"{str(channel.roomowner)}"')
                
                if channel.answer == True:
                    if len(data) == 0:
                        dbConn.insert("truthNoAdventureAnswer",f"{channel.roomowner.id},{str(channel.questionId)},1")
                    else:
                        dbConn.update("truthNoAdventureAnswer","answer = 1",f"userId == '{channel.roomowner.id}' and truthNoAdventure_id == '{channel.questionId}'")

                    count += 1
                else:
                    if len(data) == 0:
                        dbConn.insert("truthNoAdventureAnswer",f"{channel.roomowner.id},{str(channel.questionId)},0")
                    else:
                        dbConn.update("truthNoAdventureAnswer","answer = 0",f"userId == '{channel.roomowner.id}' and truthNoAdventure_id == '{channel.questionId}'")
                
                for member in channel.members:
                    if len(dbConn.selectUserById(member.user.id)) == 0:
                        dbConn.insertItem('user','id,name',f'{member.user.id},"{str(member.user)}"')
                    data = dbConn.select("*","truthNoAdventureAnswer",f"where userId == '{member.user.id}' and truthNoAdventure_id == '{channel.questionId}'")
                    if member.answer == True:
                        if len(data) == 0:
                            dbConn.insert("truthNoAdventureAnswer",f"{member.user.id},{str(channel.questionId)},1")
                        else:
                            dbConn.update("truthNoAdventureAnswer","answer = 1",f"userId == '{member.user.id}' and truthNoAdventure_id == '{channel.questionId}'")
                        count += 1
                    else:
                        if len(data) == 0:
                            dbConn.insert("truthNoAdventureAnswer",f"{member.user.id},{str(channel.questionId)},0")
                        else:
                            dbConn.update("truthNoAdventureAnswer","answer = 0",f"userId == '{member.user.id}' and truthNoAdventure_id == '{channel.questionId}'")
            
            winArray = []
            for member in channel.members:
                guess:str = ''
                answer:str = ''
                if isShow:
                    if member.answerNumber == count:
                        winArray.append(f'<@{member.user.id}>')
                        member.score += 1
                    members += f'<@{member.user.id}> 分數:{member.score}, 猜人數: {member.answerNumber}\n\n'
                else:
                    if member.answer == None:
                        answer = "還沒回答"
                    else:
                        answer = "已回答"

                    if member.answerNumber == None:
                        guess = "還沒猜"
                    else:
                        guess = "已猜"
                    members += f'<@{member.user.id}> 分數:{member.score}, 回答:{answer}, 猜人數: {guess}\n\n'

            if isShow:
                if channel.answerNumber == count:
                    winArray.append(f'<@{channel.roomowner.id}>')
                    channel.score += 1
                winer = '勝出:'
                if len(winArray) == 0:
                    winer = '勝出:沒有  '
                else:
                    for win in winArray:
                        winer += win+", "
                members = (f"<@{channel.roomowner.id}> 分數:{channel.score}, 猜人數: {channel.answerNumber}\n\n{members}選是的人數 : {count}   選否的人數: {((len(channel.members)+1)-count)}\n{winer[:-2]}")
            else:
                if channel.answer == None:
                    answer = "還沒回答"
                else:
                    answer = "已回答"

                if channel.answerNumber == None:
                    guess = "還沒猜"
                else:
                    guess = "已猜"

                members = (f"<@{channel.roomowner.id}> 分數:{channel.score}, 回答:{answer}, 猜人數: {guess}\n\n"+members)
                
            return ("題目 : " + question + "\n\n" + members)

    
    def AllAnswer(textChannelId) -> bool:
        channel = RoomDataDef.getRoomDataByTextChannelId(textChannelId)
        for member in channel.members:
            if member.answer == None:
                return False
            if member.answerNumber == None:
                return False
        return True
    
rooms = []

@app_commands.guild_only()
class TruthNoAdventureCommandGroup(app_commands.Group):

    @app_commands.command(name='創建房間')
    @app_commands.describe(題目選項='題目選項')
    @app_commands.choices(題目選項=[
        app_commands.Choice(name='現在沒得你選我懶了', value=0),
        #app_commands.Choice(name='自由出題', value=1),
    ])
    async def openRoom(self, interaction: discord.Interaction,題目選項: app_commands.Choice[int]) -> None:
        isRoomowner = RoomDataDef.isRoomowner(interaction.user.id)
        if not isRoomowner:
            if not RoomDataDef.isMember(interaction.user.id):
                categoryChannel = await interaction.guild.create_category(f'真心話不冒險 : {str(interaction.user)}')
                textChannel =await categoryChannel.create_text_channel("題目頻道")
                comminicateChannel = await categoryChannel.create_text_channel("交流頻道")
                voiceChannel = await categoryChannel.create_voice_channel("語音頻道")
                await interaction.response.send_message("創建成功",ephemeral=True)
                if interaction.user.voice != None:
                    await interaction.user.move_to(voiceChannel)
                hintMessage = await textChannel.send(f"<@{interaction.user.id}>請邀請朋友來這個文字頻道然後按加入。\n如沒有朋友請打指令：/真心話不冒險 關閉房間。")
                rooms.append({str(textChannel.id):RoomData(comminicateChannel,interaction.user,textChannel,hintMessage,voiceChannel,categoryChannel,題目選項.value,False,members=[])})
                memberMessage = await textChannel.send(RoomDataDef.getAllMemberMessageByRoomowner(textChannel.id),view=ReadyToStart())
                room = RoomDataDef.getRoomDataByRoomownerId(interaction.user.id)
                room.memberMessage = memberMessage
                room.hintMessage = hintMessage
            else:
                await interaction.response.send_message(f"<@{interaction.user.id}>你已經是遊戲成員",ephemeral=True)
        else:
            await interaction.response.send_message(f"<@{interaction.user.id}>你已經是房主",ephemeral=True)
  
    @app_commands.command(name='關閉房間')
    async def closedRoom(self, interaction: discord.Interaction) -> None:
        roomData:RoomData
        isDelete = False
        for index, room in enumerate(rooms):
            roomData = room[list(room.keys())[0]]
            if roomData.roomowner.id == interaction.user.id:
                await interaction.response.send_message('已關閉',ephemeral=True)
                await roomData.voiceChannel.delete()
                await roomData.comminicateChannel.delete()
                await roomData.textChannel.delete()
                await roomData.categoryChannel.delete()
                rooms.pop(index)
                isDelete = True
                break
        if not isDelete:
            await interaction.response.send_message('你根本就不是房主',ephemeral=True)

    @app_commands.command(name='增加題目',description="只能問是否題目，不要重複可以先看所有題目，亂加題目我一個一個捉出來打")
    async def addQuestion(self, interaction: discord.Interaction, 題目: str) -> None:
        if len(dbConn.selectUserById(interaction.user.id)) == 0:
            dbConn.insertItem('user','id,name',f'{interaction.user.id},"{str(interaction.user)}"')
        dbConn.insertItem('truthNoAdventure','user_id,question',f'"{interaction.user.id}","{題目}"')
        await interaction.response.send_message("增加成功",ephemeral=True)

    @app_commands.command(name='查看所有題目')
    async def showQuestion(self, interaction: discord.Interaction) -> None:
        questions = dbConn.select("question","truthNoAdventure","")
        json = {}
        for index, question in enumerate(questions):
            json[f"所有題目:{index+1}"] = question[0]
        await interaction.response.send_message(embed= dcInfoCommands.dcInfoCommands("","題目",0x000ff,json,False,""),ephemeral=True)

class ReadyToStart(discord.ui.View):
    
    def __init__(self, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label='加入', style=discord.ButtonStyle.primary, row=0)
    async def addToPlay(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if RoomDataDef.isOnPlayRoom(interaction.channel_id):
            if RoomDataDef.isStart(interaction.channel_id):
                await interaction.response.send_message("遊戲已開始不能加入",ephemeral=True)
            else:
                if not RoomDataDef.isRoomowner(interaction.user.id):
                    if not RoomDataDef.isMember(interaction.user.id):
                        roomDataDef = RoomDataDef.getRoomDataByTextChannelId(interaction.channel_id)
                        roomDataDef.members.append(MemberData(user = interaction.user, state=0))
                        await roomDataDef.memberMessage.edit(content= RoomDataDef.getAllMemberMessageByRoomowner(interaction.channel_id))
                        button1 = [x for x in self.children if x.label =="開始遊戲"][0]
                        button1.disabled = True
                        await interaction.response.edit_message(view=self)
                        if interaction.user.voice != None:
                            await interaction.user.move_to(roomDataDef.voiceChannel)
                    elif RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getMemberRoom(interaction.user.id).textChannel.id == interaction.channel_id:
                        await interaction.response.send_message("你已加入",ephemeral=True)
                    elif RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getMemberRoom(interaction.user.id).textChannel.id != interaction.channel_id:
                        await interaction.response.send_message(f"你去錯房間了，你的房間名稱是 真心話不冒險 : "+RoomDataDef.getMemberRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
                else:
                    if RoomDataDef.getRoomownerRoom(interaction.user.id).textChannel.id == interaction.channel_id:
                        await interaction.response.send_message("你是房主不用加入",ephemeral=True)
                    else:
                        await interaction.response.send_message("你是房主但不是這間的房主，不要去別人房間亂好不好，要加入先關閉房間，你的房間名稱是"+RoomDataDef.getRoomownerRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
        else:
            await interaction.response.send_message("你不在真心話不冒險的文字頻道",ephemeral=True)
    
    @discord.ui.button(label='準備', style=discord.ButtonStyle.primary, row=0)
    async def ready(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not RoomDataDef.isOnPlayRoom(interaction.channel_id):
            await interaction.response.send_message("你不在真心話不冒險的文字頻道",ephemeral=True)
        elif not RoomDataDef.isMember(interaction.user.id):
            await interaction.response.send_message("請先加入",ephemeral=True)
        elif RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getMemberRoom(interaction.user.id).textChannel.id != interaction.channel_id:
            await interaction.response.send_message(f"你去錯房間了，你的房間名稱是 真心話不冒險 : "+RoomDataDef.getMemberRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
        else:
            RoomDataDef.getUserData(interaction.user.id).state = 1
            await RoomDataDef.getMemberRoom(interaction.user.id).memberMessage.edit(content= RoomDataDef.getAllMemberMessageByRoomowner(interaction.channel_id))
            if RoomDataDef.isAllReady(interaction.channel_id):
                button1 = [x for x in self.children if x.label =="開始遊戲"][0]
                button1.disabled = False
                await interaction.response.edit_message(view=self)

    @discord.ui.button(label='取消準備', style=discord.ButtonStyle.primary, row=0)
    async def cancelReady(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not RoomDataDef.isOnPlayRoom(interaction.channel_id):
            await interaction.response.send_message("你不在真心話不冒險的文字頻道",ephemeral=True)
        elif not RoomDataDef.isMember(interaction.user.id):
            await interaction.response.send_message("請先加入",ephemeral=True)
        elif RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getMemberRoom(interaction.user.id).textChannel.id != interaction.channel_id:
            await interaction.response.send_message(f"你去錯房間了，你的房間名稱是 真心話不冒險 : "+RoomDataDef.getMemberRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
        elif RoomDataDef.isStart(interaction.channel_id):
                await interaction.response.send_message("遊戲已開始不能取消準備",ephemeral=True)
        else:
            RoomDataDef.getUserData(interaction.user.id).state = 0
            await RoomDataDef.getMemberRoom(interaction.user.id).memberMessage.edit(content= RoomDataDef.getAllMemberMessageByRoomowner(interaction.channel_id))
            button1 = [x for x in self.children if x.label =="開始遊戲"][0]
            button1.disabled = True
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label='開始遊戲', style=discord.ButtonStyle.primary, row=1,disabled=True)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not RoomDataDef.isOnPlayRoom(interaction.channel_id):
            await interaction.response.send_message("你不在真心話不冒險的文字頻道",ephemeral=True)
        elif not RoomDataDef.isRoomowner(interaction.user.id):
            await interaction.response.send_message("你不是房主",ephemeral=True)
        elif RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getRoomownerRoom(interaction.user.id).textChannel.id != interaction.channel_id:
            await interaction.response.send_message(f"你去錯房間了，你的房間名稱是 真心話不冒險 : "+RoomDataDef.getRoomownerRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
        elif RoomDataDef.isStart(interaction.channel_id):
            await interaction.response.send_message("遊戲已開始",ephemeral=True)
        elif len(RoomDataDef.getRoomownerRoom(interaction.user.id).members) == 0:
            await interaction.response.send_message("要至少兩個人以上，沒朋友就去找一個",ephemeral=True)
        elif not RoomDataDef.isAllReady(interaction.channel_id):
            await interaction.response.send_message("有人還沒準備好",ephemeral=True)
        else:
            RoomDataDef.getRoomownerRoom(interaction.user.id).roomStart = True
            if RoomDataDef.getRoomownerRoom(interaction.user.id).topicOptions == 0:
                await interaction.response.edit_message(content="", view=QuestionBank(room=RoomDataDef.getRoomownerRoom(interaction.user.id)))
            RoomDataDef.getQuestionInDb(interaction.channel_id)
            await RoomDataDef.getRoomDataByTextChannelId(interaction.channel_id).hintMessage.edit(content=RoomDataDef.QuestionBankDraw(interaction.channel_id,True,False))

    @discord.ui.button(label='退出房間', style=discord.ButtonStyle.primary, row=2)
    async def outRoom(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not RoomDataDef.isOnPlayRoom(interaction.channel_id):
            await interaction.response.send_message("你不在真心話不冒險的文字頻道",ephemeral=True)
        elif RoomDataDef.isMember(interaction.user.id) and RoomDataDef.getMemberRoom(interaction.user.id).textChannel.id != interaction.channel_id:
            await interaction.response.send_message(f"你去錯房間了，你的房間名稱是 真心話不冒險 : "+RoomDataDef.getMemberRoom(interaction.user.id).categoryChannel.name,ephemeral=True)
        elif RoomDataDef.isRoomowner(interaction.user.id):
            await interaction.response.send_message("你是房主，如要退出請打/真心話不冒險 關閉房間 ",ephemeral=True)
        elif not RoomDataDef.isMember(interaction.user.id):
            await interaction.response.send_message("你沒有加入任何房間",ephemeral=True)
        elif RoomDataDef.isStart(interaction.channel_id):
            await interaction.response.send_message("遊戲已開始不能退出，要有始有終一生一世不能做渣男/女玩玩就算",ephemeral=True)
        else:
            RoomDataDef.outRoom(interaction.user.id)
            await RoomDataDef.getRoomDataByTextChannelId(interaction.channel_id).memberMessage.edit(content= RoomDataDef.getAllMemberMessageByRoomowner(interaction.channel_id))
            if len(RoomDataDef.getRoomDataByTextChannelId(interaction.channel_id).members) == 0:
                button1 = [x for x in self.children if x.label =="開始遊戲"][0]
                button1.disabled = True
            elif RoomDataDef.isAllReady(interaction.channel_id):
                button1 = [x for x in self.children if x.label =="開始遊戲"][0]
                button1.disabled = False
            await interaction.response.edit_message(view=self)