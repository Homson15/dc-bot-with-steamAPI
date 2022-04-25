import os

import sqlalchemy.exc
from sqlalchemy import Column, Integer, String, create_engine, MetaData, Boolean, inspect, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlite3 import IntegrityError

from steamAPI.App import App

databaseS = None
databaseJ = None


def getDatabase():

    global databaseS

    if databaseS is None:
        databaseS = SteamDB()

    return databaseS

def getJanuszDatabase():

    global databaseJ

    if databaseJ is None:
        databaseJ = JanuszDB()

    return databaseJ



class SteamDB:

    base = create_engine("sqlite:///database/gamesInfo.db")

    MD = MetaData()

    BaseModel = declarative_base(metadata=MD)

    class GamesInfo(BaseModel):
        __tablename__ = "GamesInfo"
        appID = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        isGame = Column(Boolean, nullable=False)
        type = Column(String(100))
        parentID = Column(Integer)
        developers = Column(String(100))
        currency = Column(String(10), nullable=False)
        initialPrice = Column(Integer, nullable=False)
        discount = Column(Integer, nullable=False)
        finalFormatted = Column(String(20))

    class SubscridebGames(BaseModel):
        __tablename__ = "SubscribedGames"
        id = Column(Integer, primary_key=True)
        appID = Column(Integer, nullable=False)
        name = Column(String(100), nullable=False)
        discount = Column(Integer, nullable=False)
        finalFormatted = Column(String(20))
        serverID = Column(String(100), nullable=False)



    def __init__(self):
        self.BaseModel.metadata.create_all(self.base)
        self.mapper = inspect(self.GamesInfo)



    def putData(self, app : App):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        values = app.getValues()

        session.add(self.GamesInfo(
            appID=values["appID"],
            name=values["name"],
            isGame=values["isGame"],
            type=values["type"],
            parentID=values["parentID"],
            developers=values["developers"],
            currency=values["currency"],
            initialPrice=values["initialPrice"],
            discount=values["discount"],
            finalFormatted=values["priceFormatted"]
        ))

        session.commit()
        session.close()

    def modifyData(self, app: App):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        values = app.getValues()

        stmt = update(self.GamesInfo).where(
            self.GamesInfo.appID == app.appID
        ).values(
            appID=values["appID"],
            name=values["name"],
            isGame=values["isGame"],
            type=values["type"],
            parentID=values["parentID"],
            developers=values["developers"],
            currency=values["currency"],
            initialPrice=values["initialPrice"],
            discount=values["discount"],
            finalFormatted=values["priceFormatted"]
        ).execution_options(synchronize_session="fetch")

        session.execute(stmt)

        session.commit()
        session.close()

    def getAllRecords(self):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        arr = []

        for each in session.query(self.GamesInfo):
            arr.append(App(
                appID=each.appID,
                name=each.name,
                isGame=each.isGame,
                type=each.type,
                parent=each.parentID,
                developers=each.developers,
                currency=each.currency,
                price=each.initialPrice,
                discount=each.discount,
                finalFormatted=each.finalFormatted
            ))

        session.commit()
        session.close()

        return arr

    def getRecordByName(self, name):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        arr = []

        for each in session.query(self.GamesInfo):
            if name in each.name and each.type == 'game':
                arr.append(App(
                    appID=each.appID,
                    name=each.name,
                    isGame=each.isGame,
                    type=each.type,
                    parent=each.parentID,
                    developers=each.developers,
                    currency=each.currency,
                    price=each.initialPrice,
                    discount=each.discount,
                    finalFormatted=each.finalFormatted
                ))



        session.commit()
        session.close()

        return arr


    def getNoneType(self):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        arr = []

        for each in session.query(self.GamesInfo):
            if not each.type:
                arr.append(App(
                    appID=each.appID,
                    name=each.name,
                    isGame=each.isGame,
                    type=each.type,
                    parent=each.parentID,
                    developers=each.developers,
                    currency=each.currency,
                    price=each.initialPrice,
                    discount=each.discount,
                    finalFormatted=each.finalFormatted
                ))

        session.commit()
        session.close()

        return arr



    def subscribe(self, app : App, serverID):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        values = app.getValues()

        try:
            session.add(self.SubscridebGames(
                appID=values["appID"],
                name=values["name"],
                discount=values["discount"],
                finalFormatted=values["priceFormatted"],
                serverID=serverID
            ))
        except IntegrityError:
            return False

        session.commit()
        session.close()

        return True

    def getSubscribed(self, serverID):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        arr = []

        for each in session.query(self.SubscridebGames).where(self.SubscridebGames.serverID==serverID):
            arr.append(App(
                appID=each.appID,
                name=each.name,
                discount=each.discount,
                finalFormatted=each.finalFormatted,
                serverID=each.serverID
            ))


        session.commit()
        session.close()

        return arr

    def modifySubbscribed(self, app: App, serverID):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        stmt = update(self.SubscridebGames).where(
            self.SubscridebGames.serverID==serverID and self.SubscridebGames.appID==app.appID
            ).values(
                    bdiscount = app.discount,
                    priceFormatted = app.priceFormatted
            ).execution_options(synchronize_session="fetch")

        session.execute(stmt)

        session.commit()
        session.close()


    def deleteSubscribed(self, app: App, serverID):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        session.query(self.SubscridebGames).filter(
            self.SubscridebGames.serverID == serverID and self.SubscridebGames.appID==app.appID
        ).delete()

        session.commit()
        session.close()





class JanuszDB:

    base = create_engine("sqlite:///database/janusz.db")

    MD = MetaData()

    BaseModel = declarative_base(metadata=MD)

    class Servers(BaseModel):
        __tablename__ = "Servers"
        serverID = Column(String(100), primary_key=True)
        bindChannel = Column(String(100))


    def __init__(self):
        self.BaseModel.metadata.create_all(self.base)
        self.mapper = inspect(self.Servers)

    def getServers(self):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        arr = []

        for each in session.query(self.Servers):
            arr.append([each.serverID, each.bindChannel])


        session.commit()
        session.close()

        return arr


    def addServer(self, serverID, channelID):

        for element in self.getServers():
            if serverID == element[0]:
                return self.modifyServer(serverID, channelID)


        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        session.add(self.Servers(
            serverID = serverID,
            bindChannel = channelID
        ))

        session.commit()
        session.close()

        print(f"Channel added!")

        return True

    def modifyServer(self, serverID, channelID):


        for element in self.getServers():
            if str(channelID) == element[1]:
                return False


        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        stmt = update(self.Servers).where(self.Servers.serverID == serverID).values(
            bindChannel=channelID
            ).execution_options(synchronize_session="fetch")

        session.execute(stmt)

        session.commit()
        session.close()

        print(f"Channel modified!")

        return True


    def deleteServer(self, serverID):

        for element in self.getServers():
            if serverID == element[0]:

                DBSesion = sessionmaker(bind=self.base)
                session = DBSesion()

                session.query(self.Servers).filter(self.Servers.serverID == serverID).delete()

                print(f"Channel deleted!")

                session.commit()
                session.close()

                return True

        return False

