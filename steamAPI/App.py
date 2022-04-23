
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

        self.url = f'https://store.steampowered.com/api/appdetails?appids={appID}'

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

            self.type = data["type"]

            if self.type=="game":
                self.isGame = True
            else:
                self.parent = data["fullgame"]["appid"]

            self.developers = data["developers"][0]

            if not data["is_free"]:

                price = data["price_overview"]

                self.currency = price["currency"]
                self.initialPrice = price["initial"]
                self.finalPrice = price["final"]
                self.discount = price["discount_percent"]

                self.priceFormatted = price["final_formatted"]

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


