import os
from sqlalchemy import Column, Integer, String, create_engine, MetaData, Boolean, inspect, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from steamAPI.App import App

database = None


def getDatabase():

    global database

    if database is None:
        database = Database()

    return database



class Database:

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
        appID = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        discount = Column(Integer, nullable=False)
        finalFormatted = Column(String(20))



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

        return arr

    def getRecordByName(self, name):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        arr = []

        for each in session.query(self.GamesInfo):
            if name in each.name:
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

        return arr

    def subscribe(self, app : App):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        values = app.getValues()

        session.add(self.SubscridebGames(
            appID=values["appID"],
            name=values["name"],
            discount=values["discount"],
            finalFormatted=values["priceFormatted"]
        ))

        session.commit()
        session.close()


    def getSubscribed(self):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        arr = []

        for each in session.query(self.SubscridebGames):
            arr.append(App(
                appID=each.appID,
                name=each.name,
                discount=each.discount,
                finalFormatted=each.finalFormatted
            ))

        return arr

    def modifySubbscribed(self, app: App):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        session.query(self.SubscridebGames).update().where(self.SubscridebGames.appID==app.appID).values(
            discount = app.discount,
            priceFormatted = app.priceFormatted
        )

        session.commit()
        session.close()


    def deleteSubscribed(self, app: App):

        DBSesion = sessionmaker(bind=self.base)
        session = DBSesion()

        session.query(self.SubscridebGames).delete().where(self.SubscridebGames.appID==app.appID)

        session.commit()
        session.close()














