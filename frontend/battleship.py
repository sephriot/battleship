from kivy import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

import plane
from gamebutton import GameButton


class Battleship(GridLayout):
    isGameStarted = False

    def __init__(self, **kwargs):
        super(Battleship, self).__init__(**kwargs)
        self.ids['opponent'].disabled = True

        for c1 in self.children:
            for c2 in c1.children:
                for c3 in c2.children:
                    for c4 in c3.children:
                        if isinstance(c4, GameButton):
                            c4.sendMessage = self.sendMessage

    def startButtonClick(self):
        self.ids['player'].disabled = True
        self.ids['opponent'].disabled = False
        self.ids['startGameButton'].disabled = True
        self.ids['gameId'].disabled = True
        print("Click")
        self.isGameStarted = True

    def onMessage(self, message):
        x = int(message['x'])
        y = int(message['y'])
        self.ids['player'].ids[str(y)].ids[str(x)].setWasHit()
        if self.isShip(x, y) and self.isSunken(x, y, {}):
            self.sank(x, y, {})
        elif self.isShip(x, y):
            self.ids['opponent'].ids[str(y)].ids[str(x)].hit()
        else:
            self.ids['opponent'].ids[str(y)].ids[str(x)].miss()

    def sendMessage(self, message):
        if not self.isGameStarted:
            return

        print(message)
        self.onMessage(message)

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

    def sank(self, x, y, visited):
        if (x, y) not in visited:
            visited[(x, y)] = True
            for i in range(y - 1, y + 2):
                if i == 0 or i == 11:
                    continue
                for j in range(x - 1, x + 2):
                    if j == 0 or j == 11:
                        continue
                    self.ids['player'].ids[str(y)].ids[str(x)].setWasHit()
                    self.ids['opponent'].ids[str(y)].ids[str(x)].setWasHit()
                    if self.ids['opponent'].ids[str(y)].ids[str(x)].isShip:
                        self.sank(j, i, visited)


class BattleshipApp(App):

    def build(self):
        return Battleship()
