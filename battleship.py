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
        x = str(message['x'])
        y = str(message['y'])
        if self.isShip(x, y):
            self.ids['opponent'].ids[y].ids[x].hit()
        else:
            self.ids['opponent'].ids[y].ids[x].miss()

    def sendMessage(self, message):
        if not self.isGameStarted:
            return

        print(message)
        self.onMessage(message)

    def isShip(self, x: str, y: str):
        return self.ids['player'].ids[y].ids[x].isShip


class BattleshipApp(App):

    def build(self):
        return Battleship()


if __name__ == '__main__':
    Config.read('config.ini')
    BattleshipApp().run()
