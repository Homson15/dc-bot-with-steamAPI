import json

import requests

from steamAPI.App import App

S = None

def getSteam():

    global S
    if S is None:
        S = Steam()

    return S


class Steam:

    def __init__(self):

        self.KEY = "F4A04A3F753F55A7D6D9BEFEB35EB92C"

        SVid = 413150


        print(self.getApp(SVid))
        res = self.getAppIdByName("Witcher")
        if not isinstance(res, int):
            print(res.id, res.name, res.isDLC)




    def getAppIdByName(self, name):

        url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        request = requests.get(url).json()

        print(len(request["applist"]["apps"]))

        #print(type(request))


        for each in reversed(request["applist"]["apps"]):
            if name in each["name"]:
                try:
                    print(each["appid"], each["name"])
                    req = requests.get(f'https://store.steampowered.com/api/appdetails?appids={each["appid"]}').json()[str(each["appid"])]["data"]
                    if req["type"] == "game":
                        return App(each["appid"], each["name"], False)
                    elif req["type"] == "dlc":
                        #print(name, req["fullgame"]["name"])
                        if name in req["fullgame"]["name"]:
                            return App(req["fullgame"]["appid"], req["fullgame"]["name"], False)
                except KeyError:
                    pass

        return -1


    def getApp(self, id):

        url = f'https://store.steampowered.com/api/appdetails?appids={id}'
        return requests.get(url).text
