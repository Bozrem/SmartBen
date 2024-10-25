from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty

class AlarmDisplay(BoxLayout):
    pass

class AlarmItem:
    def __init__(self, name, time, repeat=False, sound='default', **kwargs):
        self.name = name
        self.time = time
        self.repeat = repeat
        self.sound = sound
        self.metadata = kwargs  # Holds additional info that’s not displayed initially

    def edit(self, name=None, time=None, repeat=None, sound=None):
        if name: self.name = name
        if time: self.time = time
        if repeat is not None: self.repeat = repeat
        if sound: self.sound = sound

    def get_display_info(self):
        return {
            'alarm_name': self.name,
            'alarm_time': self.time,
            'alarm_repeat': self.repeat
        }

class AlarmItemWidget(Button):
    alarm_name = StringProperty()
    alarm_time = StringProperty()
    alarm_repeat = BooleanProperty()

class AlarmScreen(Screen):
    def on_enter(self):
        status_bar = self.ids.status_bar
        widget_info = [{'name': 'BackWidget', 'position': 'left'}]
        status_bar.update_widgets(widget_info)
        
    def load_widgets(self):
        pass
    
    

    def get_alarm_data(self):
        # This method fetches alarms from the API (mocked here)
        return [
            {'name': 'Morning Alarm', 'time': '7:00 AM', 'repeat': True, 'sound': 'birds'},
            {'name': 'Meeting Alarm', 'time': '10:00 AM', 'repeat': False, 'sound': 'chimes'}
        ]

    def update_alarm_data(self, alarm_item):
        # Placeholder for API update
        pass

class ImgBtn(ButtonBehavior, Image):
    def __init__(self, on_release=None, **kwargs):
        super(ImgBtn, self).__init__(**kwargs)
        self.on_release_callback = on_release  # Store the callable

    def on_release(self):
        if self.on_release_callback:
            self.on_release_callback()  # Call the stored function