from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import json

class AlarmDisplay(BoxLayout):
    pass

# On enter, pull data from the api for the current alarms
# for each alarm pulled, pull the json data into a useable AlarmItem object
# 

class AlarmItem:
    def __init__(self, name, time, enabled, media_path, repeat):
        self.name = name
        self.time = time
        self.enabled = enabled
        self.media_path = media_path
        self.repeat = repeat
    
    @classmethod
    def from_json(cls, json_data):
        # Parse JSON data
        data = json.loads(json_data)
        
        # Create and return an instance of AlarmItem
        return cls(
            name=data["name"],
            time=data["time"],
            enabled=data["enabled"],
            media_path=data["media_path"],
            repeat=data["repeat"]
        )
    
    def to_json(self):
        pass # Will turn itself back into the json format for storage

    def to_widget(self):
        return {
            'alarm_name': self.name,
            'alarm_time': self.time,
            'alarm_repeat': self.repeat,
            'alarm_item': self  # Reference to the AlarmItem instance itself
        }

    def edit_alarm(self, refresh_callback):
        editor = EditorPopup(self, refresh_callback=refresh_callback)
        editor.open()
    

class AlarmItemWidget(RecycleDataViewBehavior, BoxLayout):
    alarm_item = ObjectProperty()  # Holds the associated AlarmItem instance
    alarm_name = StringProperty()
    alarm_time = StringProperty()
    alarm_repeat = BooleanProperty()


class AlarmScreen(Screen):
    def on_enter(self):
        self.AlarmList = []

        self.load_alarm_list()
        self.load_widgets()

        
    def load_widgets(self):
        self.ids.alarm_list.data = [item.to_widget() for item in self.AlarmList]

    def open_editor(self, alarm_item):
        alarm_item.edit_alarm(refresh_callback=self.load_widgets)
    
    def add_alarm(self):
        pass

    def load_alarm_list(self):
        # This method fetches alarms from the API (mocked here)
        mock_api_data = [
            '{"name": "Test Alarm 1", "time": "07:00:00", "enabled": true, "media_path": "~/SmartBen/data/media/alarm.mp3", "repeat": false}',
            '{"name": "Test Alarm 2", "time": "09:00:00", "enabled": false, "media_path": "~/SmartBen/data/media/alarm.mp3", "repeat": true}',
        ]
        for jsonItem in mock_api_data:
            alarm = AlarmItem.from_json(jsonItem)
            self.AlarmList.append(alarm)

class ImgBtn(ButtonBehavior, Image):
    def __init__(self, on_release=None, **kwargs):
        super(ImgBtn, self).__init__(**kwargs)
        self.on_release_callback = on_release  # Store the callable

    def on_release(self):
        if self.on_release_callback:
            self.on_release_callback()  # Call the stored function

class EditorPopup(Popup):
    alarm_item = ObjectProperty(None)  # Reference to the alarm item being edited
    refresh_callback = ObjectProperty(None)  # Callback to refresh the list

    def __init__(self, alarm_item, refresh_callback, **kwargs):
        super().__init__(**kwargs)
        self.alarm_item = alarm_item
        self.refresh_callback = refresh_callback
        self.update_inputs()

    def update_inputs(self):
        self.ids.name_input.text = self.alarm_item.name
        self.ids.time_input.text = self.alarm_item.time

    def save_changes(self):
        self.alarm_item.name = self.ids.name_input.text
        self.alarm_item.time = self.ids.time_input.text
        if self.refresh_callback:
            self.refresh_callback()  # Call the refresh callback to update the display
        self.dismiss()
