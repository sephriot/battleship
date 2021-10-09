import asyncio

from kivy import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from battleship import Battleship
from genericscreen import GenericScreen


class BattleshipApp(App):

    async def async_run(self, async_lib=None):
        sm = ScreenManager()
        sm.add_widget(Battleship(name='game'))
        sm.add_widget(GenericScreen(name='disconnect', messageText="Your partner has disconnected!"))
        sm.add_widget(GenericScreen(name='loss', messageText="You lost :("))
        sm.add_widget(GenericScreen(name='victory', messageText="You won!"))

        self.load_config()
        self.load_kv(filename=self.kv_file)
        self.root = sm
        await asyncio.gather(super(BattleshipApp, self).async_run(async_lib=async_lib),
                             self.root.get_screen('game').client.run())

    def stop(self):
        self.root.get_screen('game').client.stop()
        super(BattleshipApp, self).stop()


if __name__ == '__main__':
    Config.read('config.ini')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        BattleshipApp().async_run(async_lib='asyncio')
    )
