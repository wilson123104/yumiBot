import discord
import random
import sys
sys.path.append("..")
from function import dcInfoCommands
from db import dbConn

def drawCard(client:discord.Client):
    rNumber = random.randint(1,100)
    #rNumber = 1
    percentage_list = dbConn.select("*","card_rating","ORDER By percentage ASC")
    count = 0
    index = 0
    for percentage in percentage_list:
        if count < rNumber:
            count += percentage[2]
        else:
            break
        index += 1
    list = __get_card_list_by_percentage(percentage_list[index-1][0])
    
    if list[4] != None:
        user = client.get_user(int(list[4]))
        userData = {
            "介紹:":user.mention+list[3]
        }
        return dcInfoCommands.dcInfoCommands(user.display_avatar, "("+list[5]+") "+list[1]+"          系列: "+list[6], 0x000ff, userData, True, "")
    else:
        userData = {
            "介紹:":list[3]
        }
        return dcInfoCommands.dcInfoCommands(list[2], "("+list[5]+") "+list[1]+"          系列: "+list[6], 0x000ff, userData, True, "")

def __get_card_list_by_percentage(number:int):
    card_list = dbConn.select("c.id, c.name, c.img, c.description, c.dc_id, r.name, t.name","card c, card_rating r, card_type t",f"where card_rating_id = {number} and c.card_rating_id = r.id and c.card_type_id = t.id")
    return random.choice(card_list)