
import requests

class App:

    def __init__(self, id, name, isDLC):

        self.id = id
        self.name = name

        self.url = f'https://store.steampowered.com/api/appdetails?appids={id}'

        self.isDLC = isDLC;



    def print(self):

        print(self.id, self.name, self.isDLC)
