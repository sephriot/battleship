from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

import plane
from client import Client
from genericscreen import GenericScreen
from gamebutton import GameButton
from message import Message

Builder.load_string("""
    #: include battleship.kv
""")


class Battleship(Screen):

    def __init__(self, **kwargs):
        super(Battleship, self).__init__(**kwargs)
        self.isGameStarted = False
        self.client = Client(self.onMessage)
        self.ids['opponent'].disabled = True
        self.lastX = 0
        self.lastY = 0
        self.shipNodes = 0

        self.forEachGameField(self.registerGameFieldCallbacks)

        self.hitSound = SoundLoader.load('sounds/hit.wav')
        self.missSound = SoundLoader.load('sounds/miss.wav')
        self.positiveSound = SoundLoader.load('sounds/positive.wav')
        self.negativeSound = SoundLoader.load('sounds/negative.wav')

    def resetGameField(self, field):
        field.isShip = False
        field.wasHit = False
        field.isSunken = False
        field.updateColor()

    def registerGameFieldCallbacks(self, field):
        field.sendMessage = self.sendMessage
        field.saveLastHitPosition = self.saveLastHitPosition

    def forEachGameField(self, func):
        for c0 in self.children:
            for c1 in c0.children:
                for c2 in c1.children:
                    for c3 in c2.children:
                        for c4 in c3.children:
                            if isinstance(c4, GameButton):
                                func(c4)

    def resetUIFields(self):
        self.ids['player'].disabled = False
        self.ids['opponent'].disabled = True
        self.ids['startGameButton'].disabled = False
        self.ids['gameId'].disabled = False
        self.isGameStarted = False

    def resetGame(self):
        self.resetUIFields()
        self.forEachGameField(self.resetGameField)

    def updateShipNodes(self):
        for i in range(1, 11):
            for j in range(1, 11):
                if self.isShip(i, j):
                    self.shipNodes += 1

    def saveLastHitPosition(self, x, y):
        self.lastX = x
        self.lastY = y

    def startButtonClick(self):
        self.ids['player'].disabled = True
        self.ids['startGameButton'].disabled = True
        self.ids['gameId'].disabled = True
        print("Click")
        self.isGameStarted = True
        self.updateShipNodes()
        self.sendMessage(Message.PlayerConnectedMessage(self.ids['gameId'].text))

    def onMessage(self, message: Message.BaseMessage):

        if message.type == Message.BaseMessage.ATTACK:
            x = message.x
            y = message.y
            self.ids['player'].ids[str(y)].ids[str(x)].setWasHit()

            if self.isShip(x, y) and self.isSunken(x, y, {}):
                self.sank(x, y, {}, 'player')
                self.shipNodes -= 1
                self.sendMessage(Message.SankMessage())
                self.negativeSound.play()
                if self.shipNodes == 0:
                    self.sendMessage(Message.YouWonMessage())
                    self.manager.current = 'loss'
            elif self.isShip(x, y):
                self.shipNodes -= 1
                self.sendMessage(Message.HitMessage())
                self.hitSound.play()
            else:
                self.sendMessage(Message.MissMessage())
                self.missSound.play()
                self.myTurn()
        elif message.type == Message.BaseMessage.SANK:
            self.sank(self.lastX, self.lastY, {}, 'opponent')
            self.positiveSound.play()
            self.myTurn()
        elif message.type == Message.BaseMessage.HIT:
            self.ids['opponent'].ids[str(self.lastY)].ids[str(self.lastX)].hit()
            self.hitSound.play()
            self.myTurn()
        elif message.type == Message.BaseMessage.MISS:
            self.ids['opponent'].ids[str(self.lastY)].ids[str(self.lastX)].miss()
            self.missSound.play()
        elif message.type == Message.BaseMessage.GAME_ID_NOT_ALLOWED:
            self.gameIdNotAllowed()
        elif message.type == Message.BaseMessage.PLAYER_CONNECTED:
            if self.isGameStarted:
                self.myTurn()
        elif message.type == Message.BaseMessage.YOU_WON:
            self.manager.current = 'victory'
        elif message.type == Message.BaseMessage.PLAYER_DISCONNECTED:
            self.manager.current = 'disconnect'

    def myTurn(self):
        self.ids['opponent'].disabled = False

    def opponentTurn(self):
        self.ids['opponent'].disabled = True

    def gameIdNotAllowed(self):
        self.resetUIFields()

    def sendMessage(self, message):
        if not self.isGameStarted:
            return
        self.opponentTurn()
        self.client.sendMessage(message)

    def isShip(self, x: int, y: int):
        return self.ids['player'].ids[str(y)].ids[str(x)].isShip

    def wasHit(self, x: int, y: int):
        return self.ids['player'].ids[str(y)].ids[str(x)].wasHit

    def isSunken(self, x, y, visited):
        if not self.isShip(x, y):
            return False

        if (x, y) not in visited:
            if self.wasHit(x, y):
                visited[(x, y)] = True

                for i in range(y - 1, y + 2):
                    if i == 0 or i == 11:
                        continue
                    for j in range(x - 1, x + 2):
                        if j == 0 or j == 11 or (i == y and j == x):
                            continue
                        if self.isShip(j, i) and not self.isSunken(j, i, visited):
                            return False
            else:
                return False

        return True

    def sank(self, x, y, visited, tag="opponent"):
        if (x, y) not in visited:
            visited[(x, y)] = True
            for i in range(y - 1, y + 2):
                if i == 0 or i == 11:
                    continue
                for j in range(x - 1, x + 2):
                    if j == 0 or j == 11:
                        continue
                    self.ids[tag].ids[str(y)].ids[str(x)].setWasHit()
                    if self.ids[tag].ids[str(y)].ids[str(x)].isShip:
                        self.ids[tag].ids[str(y)].ids[str(x)].sank()
                        self.sank(j, i, visited, tag)
