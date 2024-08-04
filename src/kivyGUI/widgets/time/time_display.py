from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from datetime import datetime

class TimeDisplay(StackLayout):
    def __init__(self, **kwargs):
        super(TimeDisplay, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, *args):
        now = datetime.now()
        self.ids.date_label.text = now.strftime('%A, %B %d %Y')
        self.ids.time_label.text = now.strftime('%I:%M:%S %p').lower()
