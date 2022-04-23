
import discord
import discord as discord
from database.Database import getJanuszDatabase
from steamAPI.Steam import getSteam

from bot.Memory import Memory

b = None

def getBot():

    global b

    if b is None:
        b = Bot()

    return b


class Bot(discord.Client):

    def __init__(self):

        super().__init__()

        self.appMemory = {}


    async def on_ready(self):

        for each in getJanuszDatabase().getServers():
            channel = self.get_channel(int(each[1])) #Searches gor channel object by id from database
            #print(channel)
            if channel is None:
                continue

            await channel.send(f"Wstałem kurła")
            await channel.send(f"Czej, papiery ogarnę...")

        getSteam(False) #Execute constructor for Steam api connections

        for each in getJanuszDatabase().getServers():
            channel = self.get_channel(int(each[1])) #Searches gor channel object by id from database
            if channel is None:
                continue

            await channel.send(f"Dobra, jj")

        print("Bot is up")

    async def on_message(self, msg):

        if self.user == msg.author:
            return

        user_command = str(msg.content).split(" ")

        try:
            if user_command[0] == "kurwa":
                user_command = user_command[1:]

                if user_command[0] == "bind":
                    #print(msg.guild.id, msg.channel.id)
                    if getJanuszDatabase().addServer(msg.guild.id, msg.channel.id):
                        await msg.channel.send(f"MOJE POLE")
                    else:
                        await msg.channel.send(f"Ty debilu, ja już mam tu pole")

                elif user_command[0] == "unbind":
                    if getJanuszDatabase().deleteServer(msg.guild.id):
                        await msg.channel.send(f"Nie wypierdolisz mnie bo sam siem zwalniam!")
                    else:
                        await msg.channel.send(f"Sam spierdalaj, nawet tu nie pracuję")
                return

            print(msg.channel.id, user_command)

            for servers in getJanuszDatabase().getServers():
                if msg.channel.id == int(servers[1]):
                    #Channes is one of binded channels is Janusz's database
                    steam = getSteam()
                    if user_command[0].lower() == "search":
                        user_command = user_command[1:]
                        arg = ' '.join(str(e) for e in user_command)     #Join command back to one string
                        if arg:                                         #If no arguemnt is given, than Database searches for any argument. We don't want that
                            #print(arg)
                            arr = steam.getAppArrWithName(arg)
                            arraylen = len(arr)
                            self.appMemory[f"{msg.guild.id}"] = Memory(arr)
                            if arraylen > 5:
                                await msg.channel.send(f"Znaleziono {arraylen} wyników \naby je pokazać napisz 'show'")
                            else:
                                await msg.channel.send(f"Znaleziono: \n#")
                                i=0
                                for element in arr:
                                    data = element.getValues()
                                    await msg.channel.send(
                                        f"Index: {i}\n"
                                        f"ID: {data['appID']}\n"
                                        f"Name: {data['name']}\n"
                                        f"Initial price: {float(data['initialPrice']) / 100}\n"
                                        f"Dicount: {data['discount'] > 0}\n"
                                        f"Final Price: {data['priceFormatted']}\n"
                                    )
                                    await msg.channel.send(f"#\n")
                                    i+=1

                        else:
                            await msg.channel.send(f"Kobieto, powiedz co masz na myśli...")
                            await msg.channel.send(f"Ułatw zapracowanemu człowiekowi robotę")
                            print(f"EROOR: Given empty array as argument")


                    elif user_command[0].lower() == 'show':
                        user_command = user_command[1:]
                        #print(self.appMemory.keys(),  f"{msg.guild.id}")
                        if f"{msg.guild.id}" in self.appMemory:
                            #print("kutwa")
                            memory = self.appMemory[f"{msg.guild.id}"]
                            #print(user_command)
                            if user_command:                            #if user input is not empty after 'show'
                                if user_command[0].lower() == "next":
                                    memory.getNextInstance()
                                elif user_command[0].lower() == "prev":
                                    memory.getPrevInstance()

                            await msg.channel.send(memory.getInstance())
                            print("this instance of memory")

                    elif user_command[0].lower() == 'add':
                        user_command = user_command[1:]
                        if f"{msg.guild.id}" in self.appMemory:
                            if user_command:
                                response = getSteam().subscribe(self.appMemory[f"{msg.guild.id}"].apparr[int(user_command[0])].getValues()["appID"], msg.guild.id)
                                print("added by index")
                            else:
                                response = getSteam().subscribe(self.appMemory[f"{msg.guild.id}"].getApp().getValues()["appID"], msg.guild.id)
                                print("added automaticly")
                            if not response:
                                await msg.channel.send(f"Coś się zjebało")
                                await msg.channel.send(f"Rekord istnieje, albo aplikacja nie jest grą")
                        else:
                            await msg.channel.send(f"Przed wyruszeniem, należy przeszukać gry")

                    elif user_command[0].lower() == "subed":
                        response = getSteam().getSubscribed(msg.guild.id)
                        for element in response:
                            data = element.getValues()
                            await msg.channel.send(f"ID: {data['appID']}\n"\
                                                   f"Name: {data['name']}\n"\
                                                   f"Dicount: {data['discount'] > 0}\n"\
                                                   f"Final Price: {data['priceFormatted']}\n")


        except IndexError:
            pass
