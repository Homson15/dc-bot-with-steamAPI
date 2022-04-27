from steamAPI.App import App

class Memory:

    def __init__(self, apparr):

        self.apparr = apparr
        self.index = 0


    def getInstance(self):
        data = self.apparr[self.index].getValues()
        return (
                f"ID: {data['appID']}\n"
                f"Name: {data['name']}\n"
                #f"Type: {data['type']}\n"
                f"Initial price: {float(data['initialPrice']) / 100}\n"
                f"Currency: {data['currency']}\n"
                f"Dicount: {data['discount']}%\n"
                #f"Final Price: {data['priceFormatted']}\n"
                f"<--Prev {self.index} Next->>\n"
        )

    def getNextInstance(self):
        self.index+=1

    def getPrevInstance(self):
        self.index-=1

    def getApp(self):
        return self.apparr[self.index]