from kivy import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

import plane


class Battleship(GridLayout):

    def __init__(self, **kwargs):
        super(Battleship, self).__init__(**kwargs)
        self.ids['opponent'].disabled = True

    def startButtonClick(self):
        self.ids['player'].disabled = True
        self.ids['opponent'].disabled = False
        self.ids['startGameButton'].disabled = True
        self.ids['gameId'].disabled = True
        print("Click")


class BattleshipApp(App):

    def build(self):
        return Battleship()


if __name__ == '__main__':
    Config.read('config.ini')
    BattleshipApp().run()
