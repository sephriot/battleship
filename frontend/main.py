from kivy import Config

from battleship import BattleshipApp

if __name__ == '__main__':
    Config.read('config.ini')
    BattleshipApp().run()
