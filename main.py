import requests


url = "https://discord.com/api/v10/applications/1022527238895313013/guilds/1022529624661557298/commands/1029229224697004133"


# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot MTAyMjUyNzIzODg5NTMxMzAxMw.G0hot7.3LLltwkkpzp4Yld9r30pe-5eDtsqcnpCSKi7qo"
}



r = requests.delete(url, headers=headers)
print(r)