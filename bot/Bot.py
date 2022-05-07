import asyncio
import random

import discord
import discord as discord
from database.Database import getJanuszDatabase
from steamAPI.Steam import getSteam

from discord_components import DiscordComponents, Button, ButtonStyle, ComponentsBot, Interaction

b = None

def getBot():

    global b

    if b is None:
        b = Bot()

    return b


class Bot(discord.Client):

    def __init__(self):

        super().__init__()

        DiscordComponents(self)

        self.appMemory = {}
        self.password = 0


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
        self.generatePassword()
        await self.timeListener()

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

                elif user_command[0].lower() == "fill":
                    user_command = user_command[1:]
                    if user_command[0].lower() == "empty":
                        user_command = user_command[1:]
                        if user_command[0] == str(self.password):
                            self.generatePassword()
                            getSteam().fillNone()
                return


            for servers in getJanuszDatabase().getServers():
                if msg.channel.id == int(servers[1]):
                    #Channes is one of binded channels is Janusz's database
                    print(msg.channel.id, user_command)
                    steam = getSteam()
                    if user_command[0].lower() == "search":
                        user_command = user_command[1:]
                        arg = ' '.join(str(e) for e in user_command)     #Join command back to one string
                        if arg:                                         #If no arguemnt is given, than Database searches for any argument. We don't want that
                            #print(arg)
                            arr = steam.getAppArrWithName(arg)
                            #await msg.channel.send(f"Znaleziono {len(arr)} rekordów")

                            await self.set_menu(msg, arr)

                        else:
                            await msg.channel.send(f"Kobieto, powiedz co masz na myśli...")
                            await msg.channel.send(f"Ułatw zapracowanemu człowiekowi robotę")
                            print(f"EROOR: Given empty array as argument")

                    elif user_command[0].lower() == 'update':
                        user_command = user_command[1:]
                        if user_command:
                            if steam.updateRecord(int(user_command[0])):
                                await msg.channel.send(f"Pobrano wartości na nowo dla {user_command[0]}")
                            else:
                                await msg.channel.send(f"Coś poszło nie tak przy aktualizowaniu danych")


                    elif user_command[0].lower() == 'show':
                        user_command = user_command[1:]
                        #print(self.appMemory.keys(),  f"{msg.guild.id}")
                        if f"{msg.guild.id}" in self.appMemory:
                            #print("kutwa")
                            memory = self.appMemory[f"{msg.guild.id}"]
                            #print(user_command)
                            if user_command:                            #if user input is not empty after 'show'
                                if user_command[0].lower() == "next":
                                    await memory.getNextInstance().edit(embed=memory.getEmbedMessage())
                                elif user_command[0].lower() == "prev":
                                    await memory.getPrevInstance().edit(embed=memory.getEmbedMessage())



                    elif user_command[0].lower() == 'sub':
                        user_command = user_command[1:]
                        if user_command:
                            if user_command[0].lower() == 'index':
                                user_command = user_command[1:]
                                if f"{msg.guild.id}" in self.appMemory:
                                    if user_command:
                                        response = getSteam().subscribe(self.appMemory[f"{msg.guild.id}"].apparr[int(user_command[0])].getValues()["appID"], msg.guild.id)
                                        await msg.channel.send(f"Got it")
                                        print("added by index")
                                    else:
                                        response = getSteam().subscribe(self.appMemory[f"{msg.guild.id}"].getApp().getValues()["appID"], msg.guild.id)
                                        await msg.channel.send(f"Got it")
                                        print("added automaticly")
                                    if not response:
                                        await msg.channel.send(f"Coś się zjebało")
                                        await msg.channel.send(f"Rekord istnieje, albo aplikacja nie jest grą")
                                else:
                                    await msg.channel.send(f"Przed wyruszeniem, należy przeszukać gry")
                            elif user_command[0].lower() == 'id':
                                user_command = user_command[1:]
                                if user_command:
                                    for appid in user_command:
                                        response = getSteam().subscribe(int(appid), msg.guild.id)
                                        print("added by index")
                                        if not response:
                                            await msg.channel.send(f"Coś się zjebało")
                                            await msg.channel.send(f"Czy na pewno chciałeś {appid}?")
                                        else:
                                            await msg.channel.send(f"Dodaję {appid}")

                    elif user_command[0].lower() == "subed":
                        response = getSteam().getSubscribed(msg.guild.id)
                        await self.set_menu(msg, response)

                    elif user_command[0].lower() == "unsub":
                        user_command = user_command[1:]
                        if user_command:
                            for appid in user_command:
                                steam.unsubscribe(int(appid), msg.guild.id)
                                await msg.channel.send(f"Wyjebano chuja z bazy")



        except IndexError:
            pass


    def generatePassword(self):

        self.password = random.randint(0, 99999999)
        print(self.password)


    async def timeListener(self):
        while True:
            for server in getJanuszDatabase().getServers():
                channel = self.get_channel(int(server[1]))


                #await channel.send(f"Skanowanie promek Bzz Bzz\n")
                print("Checking for discounts...")

                ret = getSteam().checkSubscribed(int(server[0]))
                if len(ret) > 0:
                    #channel = self.get_channel(server[1])
                    await channel.send(f"A KURŁA PROMKI JAK W LIDLU!!!!\n")
                    for app in ret:
                        await channel.send(
                            f"{app.name}\n"
                            f"Promka {app.discount} %\n"
                            f"{app.finalPrice}"
                        )


            await asyncio.sleep(60 * 15) # 60 sec * 15 = 15 minutes


    async def on_button_click(self, interaction):

        try:
            if interaction.guild.id in getJanuszDatabase().getServers()[0]:

                memory = self.appMemory[f"{interaction.guild.id}"]

                if interaction.custom_id.endswith("LeftButton"):

                    await self.edit_menu(memory, move="prev")

                elif interaction.custom_id.endswith("RightButton"):

                    await self.edit_menu(memory, move="next")

                elif interaction.custom_id.endswith("Refresh"):

                    if memory.refresh():
                        await self.edit_menu(memory)
                    else:
                        await interaction.respond(content="Coś śmierdzi... Chyba nic na to nie poradzę")
                    pass

        except KeyError: #It happenes when someone presses button from past session and no "memory" is present
            pass

        if interaction.responded:
            return

        try:
            await interaction.respond(content="")
        except discord.errors.HTTPException:
            pass


    async def set_menu(self, msg, appArr):

        memory = self.appMemory[f"{msg.guild.id}"] = Memory(appArr)
        memory.setMSG(await self.print_menu(msg, memory))

    async def print_menu(self, msg, memory):


        sendMSG = await msg.channel.send(
            embed=memory.getEmbedMessage(),
            components=[[Button(style=3, label="←", custom_id=f"{msg.guild.id}LeftButton"),
                         Button(style=1, label="🔄", custom_id=f"{msg.guild.id}Refresh"),
                         Button(style=4, label="→", custom_id=f"{msg.guild.id}RightButton")]]
        )
        return sendMSG

    async def edit_menu(self, memory, move="none"):

        if move == "next":
            msg = memory.getNextInstance()
        elif move == "prev":
            msg = memory.getPrevInstance()
        else:
            msg = memory.msg

        if msg:
            await msg.edit(
                embed=memory.getEmbedMessage(),
                components=[[Button(style=3, label="←", custom_id=f"{msg.guild.id}LeftButton"),
                             Button(style=1, label="🔄", custom_id=f"{msg.guild.id}Refresh"),
                             Button(style=4, label="→", custom_id=f"{msg.guild.id}RightButton")]]
            )
        else:
            print("No Message in memory!")


class Memory:

    def __init__(self, apparr):

        self.apparr = apparr
        self.index = 0
        self.msg = None


    def getInstance(self):
        data = self.apparr[self.index].getValues()
        return (
                f"ID: {data['appID']}\n"
                #f"Name: {data['name']}\n"
                f"Type: {data['type']}\n"
                f"Initial price: {float(data['initialPrice']) / 100}\n"
                #f"Currency: {data['currency']}\n"
                f"Dicount: {data['discount']}%\n"
                f"Final Price: {data['priceFormatted']}\n"
                #f"<--Prev {self.index} Next->>\n"
        )

    def getEmbedMessage(self):
        data = self.apparr[self.index].getValues()
        embed = discord.embeds.Embed(title=f'{data["name"]}\n{self.index+1}/{len(self.apparr)}', description=self.getInstance(), color=discord.colour.Colour.random())

        return embed

    def refresh(self):
        if self.apparr[self.index].selfSetValues():
            return getSteam().updateRecordByApp(self.apparr[self.index])
        return False

    def getNextInstance(self):
        self.index+=1
        self.index = self.index % len(self.apparr)
        return self.msg

    def getPrevInstance(self):
        self.index-=1
        self.index = self.index % len(self.apparr)
        return self.msg

    def getApp(self):
        return self.apparr[self.index]

    def setMSG(self, msg):
        self.msg = msg