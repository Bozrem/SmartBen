from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from widgets.status.status_bar import StatusBar
from widgets.time.time_display import TimeDisplay, TimeScreen
from widgets.weather.weather_display import WeatherDisplay, WeatherScreen
from widgets.alarm.alarm_display import AlarmDisplay, AlarmScreen
from widgets.media.media_display import MediaDisplay, MediaScreen


Window.borderless = True

class MainScreen(Screen):
    def on_enter(self):
        status_bar = self.ids.status_bar
        widget_info = [
            {'name': 'VolumeWidget', 'position': 'left'},
            {'name': 'BrightnessWidget', 'position': 'left'},
            {'name': 'BluetoothWidget', 'position': 'left'},
            {'name': 'WeatherWidget', 'position': 'center'},
            {'name': 'SettingsWidget', 'position': 'right'},
        ]
        status_bar.update_widgets(widget_info)

class SmartBen(App):
    def build(self):
        # Load the KV files
        Builder.load_file('SmartBen.kv')
        Builder.load_file('src/kivyGUI/widgets/weather/weather_display.kv')
        Builder.load_file('src/kivyGUI/widgets/time/time_display.kv')
        Builder.load_file('src/kivyGUI/widgets/alarm/alarm_display.kv')
        Builder.load_file('src/kivyGUI/widgets/media/media_display.kv')
        Builder.load_file('src/kivyGUI/widgets/status/status_bar.kv')

        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(WeatherScreen(name='weather_screen'))
        sm.add_widget(TimeScreen(name='time_screen'))
        sm.add_widget(AlarmScreen(name='alarm_screen'))
        sm.add_widget(MediaScreen(name='media_screen'))

        
        return sm
    
    def show_volume_popup(self):
        # TODO make more consise
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Volume'))
        slider = Slider(min=0, max=100, value=50)
        layout.add_widget(slider)
        close_button = Button(text='Close', size_hint_y=0.2)
        layout.add_widget(close_button)

        slider.bind(value=self.on_volume_change)
        
        popup = Popup(title='Volume Control', content=layout, size_hint=(0.8, 0.4))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def show_brightness_popup(self):
        # TODO make more consise
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Brightness'))
        slider = Slider(min=0, max=100, value=50)
        layout.add_widget(slider)
        close_button = Button(text='Close', size_hint_y=0.2)
        layout.add_widget(close_button)

        slider.bind(value=self.on_brightness_change)
        
        popup = Popup(title='Brightness Control', content=layout, size_hint=(0.8, 0.4))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def on_volume_change(self, instance, value):
        print(f"Volume changed to {value}%")
        # TODO

    def on_brightness_change(self, instance, value):
        print(f"Brightness changed to {value}%")
        # TODO

if __name__ == '__main__':
    SmartBen().run()
