import discord
client: discord.Client
token:str
target:str

def setClient(client1):
    global client 
    client = client1

def setToken(token1):
    global token 
    token = token1

def setTarget(target1):
    global target 
    target = target1