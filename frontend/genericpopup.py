from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class GenericPopup(BoxLayout):
    messageText = StringProperty("")
    approveText = StringProperty("")
    cancel = ObjectProperty()
    approve = ObjectProperty()

    def __init__(self, **kwargs):
        super(GenericPopup, self).__init__(**kwargs)
