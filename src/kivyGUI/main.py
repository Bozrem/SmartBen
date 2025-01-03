from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import ConfigParser
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from widgets.status.status_bar import StatusBar
from widgets.time.time_display import TimeDisplay
from widgets.weather.weather_display import WeatherDisplay, WeatherScreen
from widgets.alarm.alarm_display import AlarmDisplay, AlarmScreen
from widgets.media.media_display import MediaDisplay, MediaScreen


Window.borderless = True
Window.size = (800, 480)

# -----------------------------
# Global Helper Classes
# -----------------------------

class ImgBtn(ButtonBehavior, Image):
    def __init__(self, on_release=None, **kwargs):
        super(ImgBtn, self).__init__(**kwargs)
        self.on_release_callback = on_release  # Store the callable

    def on_release(self):
        if self.on_release_callback:
            self.on_release_callback()  # Call the stored function

# -----------------------------
# Main Page
# -----------------------------

class MainScreen(Screen):
    def on_enter(self):
        status_bar = self.ids.status_bar
        widget_info = [
            {'name': 'VolumeWidget', 'position': 'left'},
            {'name': 'BrightnessWidget', 'position': 'left'},
            {'name': 'BluetoothWidget', 'position': 'left'},
            {'name': 'WeatherDisplay', 'position': 'center'},
            {'name': 'SettingsWidget', 'position': 'right'},
        ]
        status_bar.update_widgets(widget_info)

class SmartBen(App):
    def build(self):
        self.config = ConfigParser()
        self.config.read('src/kivyGUI/style.ini')

        self.background_color = [float(x) for x in self.config.get('colors', 'background_color').split(',')]
        self.text_color = [float(x) for x in self.config.get('colors', 'text_color').split(',')]
        self.large_font_size = self.config.get('fonts', 'large_font_size')
        self.medium_font_size = self.config.get('fonts', 'medium_font_size')
        self.medium_small_font_size = self.config.get('fonts', 'medium_small_font_size')
        self.small_font_size = self.config.get('fonts', 'small_font_size')


        Builder.load_file('SmartBen.kv')
        Builder.load_file('src/kivyGUI/widgets/weather/weather_display.kv')
        Builder.load_file('src/kivyGUI/widgets/time/time_display.kv')
        Builder.load_file('src/kivyGUI/widgets/alarm/alarm_display.kv')
        Builder.load_file('src/kivyGUI/widgets/media/media_display.kv')
        Builder.load_file('src/kivyGUI/widgets/status/status_bar.kv')

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(WeatherScreen(name='weather_screen'))
        sm.add_widget(AlarmScreen(name='alarm_screen'))
        sm.add_widget(MediaScreen(name='media_screen'))

        return sm
    
    def show_volume_popup(self):
        popup = VolumePopup()
        popup.open()

    # Method to show brightness popup
    def show_brightness_popup(self):
        popup = BrightnessPopup()
        popup.open()

    def on_volume_change(self, instance, value):
        print(f"Volume changed to {value}%")
        # TODO integrate with APIs

    def on_brightness_change(self, instance, value):
        print(f"Brightness changed to {value}%")
        # TODO add command to change this

class VolumePopup(Popup):
    pass

class BrightnessPopup(Popup):
    pass

if __name__ == '__main__':
    SmartBen().run()
