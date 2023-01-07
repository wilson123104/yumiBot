import discord
import configload 

client: discord.Client
token:str
target:str
textChannel = configload.getConfigSetting("Credentials", "TextChannel")
chatAICookie = configload.getConfigSetting("Credentials", "ChatAICookie")

def setClient(client1):
    global client 
    client = client1

def setToken(token1):
    global token 
    token = token1

def setTarget(target1):
    global target 
    target = target1