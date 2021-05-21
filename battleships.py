from kivy import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

import plane


class Battleships(GridLayout):

    def __init__(self, **kwargs):
        super(Battleships, self).__init__(**kwargs)


class BattleshipsApp(App):

    def build(self):
        return Battleships()


if __name__ == '__main__':
    Config.read('config.ini')
    BattleshipsApp().run()
