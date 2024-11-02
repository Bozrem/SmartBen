from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
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
        # Create an AlarmItemWidget initialized with this alarm's data
        return {
            'alarm_name': self.name,
            'alarm_time': self.time,
            'alarm_repeat': self.repeat
        }
        # Create and return a new AlarmItemWidget that can be added to the recycle layout
    

class AlarmItemWidget(RecycleDataViewBehavior, BoxLayout):
    alarm_name = StringProperty()
    alarm_time = StringProperty()
    alarm_repeat = BooleanProperty()

class AlarmScreen(Screen):
    def on_enter(self):
        self.AlarmList = []
        status_bar = self.ids.status_bar
        widget_info = [{'name': 'BackWidget', 'position': 'left'}]
        status_bar.update_widgets(widget_info)

        self.load_alarm_list()
        for alarm in self.AlarmList:
            print(alarm) # debugging
        self.load_widgets()

        
    def load_widgets(self):
        rView = self.ids.alarm_list
        rView.data = []
        for alarm in self.AlarmList:
            rView.data.append(alarm.to_widget())
    
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