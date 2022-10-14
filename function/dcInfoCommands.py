from discord import Embed

def dcInfoCommands(thumbnail, title, color:any, data:dict[str, any], inline:bool, footer:str):
    embed = Embed(title=title, color=0x000ff)
    for [fieldName, fieldVal] in data.items():
        embed.add_field(name=fieldName,value=fieldVal,inline=inline)
    embed.set_footer(text=footer)
    embed.set_thumbnail(url=thumbnail)
    return embed
