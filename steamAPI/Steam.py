import requests
import os

from steamAPI.App import App
from database.Database import getDatabase

S = None

def getSteam(FLAG=True):

    global S
    if S is None:
        S = Steam(FLAG)

    return S


class Steam:

    def __init__(self, FLAG):

        self.KEY = "F4A04A3F753F55A7D6D9BEFEB35EB92C"

        """
        SVid = 413150

        print(self.getApp(SVid).getValues()) #testy dla id stardew Valley

        
        res = self.getAppIdByName("Witcher") #testy wyszukiwania
        if not isinstance(res, int):
            res.selfSetValues();
            print(res.getValues())
        """
        if FLAG:
            if not os.path.exists(os.path.join("database", "gamesInfo.db")):
                self.gatherData()
            else:
                self.updateData()

        #self.getAppArrWithName("PAYDAY")



    def gatherData(self):

        if os.path.exists(os.path.join("database", "gamesInfo.db")):
            print("[!] File already exists, try updateData() method...")

        print(f"Gathering new data from Steam ...")

        url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        request = requests.get(url)
        file = request.json()

        db = getDatabase()

        #print(request["applist"]["apps"][0])

        for each in file["applist"]["apps"]:
            #print(each["appid"])
            app = App(each["appid"], each["name"])
            app.selfSetValues()
            print(f"Adding {app.name}")
            db.putData(app)


    def updateData(self):

        print(f"Gathering new data from Steam ...")

        db = getDatabase()

        data = db.getAllRecords()

        url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        request = requests.get(url)
        file = request.json()

        arr = []

        for element in data:
            arr.append(element.appID)

        for each in file["applist"]["apps"]:
            if not each["appid"] in arr:
                app = App(each["appid"], each["name"])
                app.selfSetValues(False)
                #print("Found new values for database")
                print(f"Adding {app.appID} ({app.name})")
                db.putData(app)
            else:
                #print(f"{each['appid']} ({each['name']}) is already in database")
                pass

        print("All is up to date!")



    def getAppArrWithName(self, name):
        ret = getDatabase().getRecordByName(name, True)

        if not len(ret):
            ret = getDatabase().getRecordByName(name)

        return ret



    def subscribe(self, appid : int, serverID):

        app = self.getApp(appid)
        data = self.getSubscribed(serverID)


        for element in data:
            if appid == element.appID:
                return False


        if app.appID != 0:
            return getDatabase().subscribe(app, serverID)
        return False


    def checkSubscribed(self, serverID):

        db = getDatabase()

        apps = db.getSubscribed(serverID)

        discounted = []

        for app in apps:
            oldDiscount = app.discount
            app.selfSetValues()
            if app.discount != oldDiscount:
                if app.discount > oldDiscount:
                    discounted.append(app)
                db.modifySubbscribed(app)
        return discounted

    def getSubscribed(self, serverID):
        return getDatabase().getSubscribed(serverID)



    def unsubscribe(self, appid: int, serverID):
        getDatabase().deleteSubscribed(App(appid, "Whatever"), serverID)




    def getApp(self, appid: int):

        url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
        request = requests.get(url)
        file = request.json()

        try:
            if file:

                name = file[f"{appid}"]["data"]["name"]

                app = App(appid, name)
                if app.selfSetValues():
                    return app
                else:
                    return App(0,"Error!")

            else:
                return App(0,"Error!")
        except KeyError:
            return App(0,"Error!")


    def fillNone(self):
        print(f"Scanning empty records")

        db = getDatabase()

        data = db.getNoneType()

        #url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        #request = requests.get(url)
        #file = request.json()

        for element in data:
            if not element.getValues()["type"]:
                app = App(element.getValues()["appID"], element.getValues()["name"])
                app.selfSetValues(False)
                if app.type:
                    db.modifyData(app)
                    print(f"changed {app.name}")


        #print("All is up to date!")


    def updateRecord(self, appID : int):

        app = self.getApp(appID)
        if app.selfSetValues():
            print(app.getValues())
            return getDatabase().modifyData(app)

        return False
