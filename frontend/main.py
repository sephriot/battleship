import asyncio

from kivy import Config

from battleship import BattleshipApp

if __name__ == '__main__':
    Config.read('config.ini')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        BattleshipApp().async_run(async_lib='asyncio')
    )
