
import requests

class App:

    def __init__(self, appID, name, isGame=False, type=None, parent=None, developers=None, currency="PLN", price=0, finalPrice=0, discount=0, finalFormatted="", serverID=0):

        self.appID = appID
        self.name = name

        self.isGame = isGame
        self.type = type
        self.parent = parent
        self.developers = developers
        self.currency = currency
        self.initialPrice = price
        self.finalPrice = finalPrice
        self.discount = discount
        self.priceFormatted = finalFormatted
        self.serverID = serverID

        self.url = f'https://store.steampowered.com/api/appdetails?appids={appID}&currency=25'

        self.valuesSet = False

    def selfSetValues(self, printFLAG=True):

        request = requests.get(self.url)
        file = request.json()


        if not file:
            if printFLAG:
                print(f"Request returns NULL for {self.appID} ({self.name})")
            return False

        try:
            data = file[f"{self.appID}"]["data"]

            #print("APPID/DATA")

            self.type = data["type"]

            #print(f"TYPE: {self.type}")

            if self.type=="game":
                self.isGame = True
            else:
                self.parent = data["fullgame"]["appid"]

            self.developers = data.get("developers", [])[0]

            #print("DEVS")

            if "is_free" in data:

                price = data["price_overview"]

                #print("PRICE")

                self.currency = price["currency"]
                self.initialPrice = price["initial"]
                self.finalPrice = price["final"]
                self.discount = price["discount_percent"]

                #print("ELSE")

                self.priceFormatted = price["final_formatted"]

                #print("FORMATED")


            self.valuesSet = True

            return True

        except KeyError:
            if printFLAG:
                print(f"Error while geting values for {self.appID} ({self.name}) \n"
                      f"Gathering data stopped...")
            return False

    def getValues(self):

        return {"appID": self.appID, "name": self.name, "isGame": self.isGame, "type": self.type, "parentID": self.parent,
                "developers": self.developers, "currency": self.currency, "initialPrice": self.initialPrice, "finalPrice": self.finalPrice,
                "discount": self.discount, "priceFormatted": self.priceFormatted, "serverID": self.serverID}


