import requests
import os

from steamAPI.App import App
from database.Database import getDatabase

S = None

def getSteam():

    global S
    if S is None:
        S = Steam()

    return S


class Steam:

    def __init__(self):

        self.KEY = "F4A04A3F753F55A7D6D9BEFEB35EB92C"

        """
        SVid = 413150

        print(self.getApp(SVid).getValues()) #testy dla id stardew Valley

        
        res = self.getAppIdByName("Witcher") #testy wyszukiwania
        if not isinstance(res, int):
            res.selfSetValues();
            print(res.getValues())
        """

        if not os.path.exists(os.path.join("database", "gamesInfo.db")):
            self.gatherData()

        self.getAppArrWithName("PAYDAY")



    def gatherData(self):

        print(f"Gathering new data from Steam ...")

        url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        request = requests.get(url).json()

        db = getDatabase()

        print(request["applist"]["apps"][0])

        for each in request["applist"]["apps"]:
            #print(each["appid"])
            app = App(each["appid"], each["name"])
            if app.selfSetValues():
                print(f"Adding {app.name}")
                db.putData(app)


    def getAppArrWithName(self, name):

        data = getDatabase().getRecordByName(name)

        arr = []

        for each in data:
            arr.append(each.getValues())

        return arr




    def subscribe(self, appid : int):

        app = self.getApp(appid)

        if app.appID != 0:
            getDatabase().subscribe(app)


    def checkSubscribed(self):

        db = getDatabase()

        apps = db.getSubscribed()

        discounted = []

        for app in apps:
            oldDiscount = app.discount
            app.selfSetValues()
            if app.discount < oldDiscount:
                discounted.append(app)
                db.modifySubbscribed(app)

        return discounted


    def unsubscribe(self, appid: int):

        getDatabase().deleteSubscribed(App(appid, "Whatever"))




    def getApp(self, appid: int):

        url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
        request = requests.get(url).json()

        if request:

            name = request[f"{appid}"]["data"]["name"]

            app = App(appid, name)
            if app.selfSetValues():
                return app
            else:
                return App(0,"Error!")

        else:
            return App(0,"Error!")

