from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class GenericScreen(Screen):
    messageText = StringProperty("")

    def __init__(self, **kwargs):
        super(GenericScreen, self).__init__(**kwargs)
