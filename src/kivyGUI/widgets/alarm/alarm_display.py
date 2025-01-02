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
import os

class AlarmDisplay(BoxLayout):
    pass

# On enter, pull data from the api for the current alarms
# for each alarm pulled, pull the json data into a useable AlarmItem object
# Build each alarm item to a widget and add it to the list

# TODO:
# Pull and associate actual media paths
# Get time editor working

class AlarmItem:
    def __init__(self, name, time, enabled: bool, media_path, repeat: bool, volume_gradient: bool, light_gradient: bool, days, refresh_callback):
        self.name = name
        self.time = time
        self.enabled = enabled
        self.media_path = media_path
        self.repeat = repeat
        self.volume_gradient = volume_gradient
        self.light_gradient = light_gradient
        # Directly use the passed-in days array
        self.days = days  # Ensure `days` is a list with 7 boolean values
        self.refresh_callback = refresh_callback
        print("Initialized AlarmItem:", self.days)

    @classmethod
    def from_json(cls, json_data, callback):
        # Parse JSON data
        data = json.loads(json_data)
        # Generate days list as boolean values for each character in `data["days"]`
        days = [char == "1" for char in data["days"]]

        # Create and return an instance of AlarmItem
        return cls(
            name=data["name"],
            time=data["time"],
            enabled=data["enabled"],
            media_path=data["media_path"],
            repeat=data["repeat"],
            volume_gradient=data["volume"],
            light_gradient=data["light"],
            days=days,  # Pass the correctly formatted days list
            refresh_callback=callback
        )

    def to_widget(self):
        """Convert alarm data into a widget-friendly dictionary format."""
        # Ensure that `days` contains 7 items to match each day of the week
        assert len(self.days) == 7, "Days list should contain exactly 7 items."

        return {
            'alarm_name': self.name,
            'alarm_time': self.time,
            'alarm_enabled': self.enabled,
            'alarm_item': self,
            'sunday_active': self.days[0],
            'monday_active': self.days[1],
            'tuesday_active': self.days[2],
            'wednesday_active': self.days[3],
            'thursday_active': self.days[4],
            'friday_active': self.days[5],
            'saturday_active': self.days[6]
        }
    

class AlarmItemWidget(RecycleDataViewBehavior, BoxLayout):
    alarm_item = ObjectProperty()  # Holds the associated AlarmItem instance
    alarm_name = StringProperty()
    alarm_time = StringProperty()
    alarm_enabled = BooleanProperty()

        # Properties for each day
    sunday_active = BooleanProperty(False)
    monday_active = BooleanProperty(False)
    tuesday_active = BooleanProperty(False)
    wednesday_active = BooleanProperty(False)
    thursday_active = BooleanProperty(False)
    friday_active = BooleanProperty(False)
    saturday_active = BooleanProperty(False)

        # Define colors for active/inactive days
    active_color = (0.5, 0.8, 1, 1)  # Light blue for active
    inactive_color = (0.4, 0.4, 0.4, 1)  # Dark gray for inactive

    def update_day_colors(self):
        """Update the font color of each day label based on its active/inactive state."""
        self.ids.sunday.color = self.active_color if self.sunday_active else self.inactive_color
        self.ids.monday.color = self.active_color if self.monday_active else self.inactive_color
        self.ids.tuesday.color = self.active_color if self.tuesday_active else self.inactive_color
        self.ids.wednesday.color = self.active_color if self.wednesday_active else self.inactive_color
        self.ids.thursday.color = self.active_color if self.thursday_active else self.inactive_color
        self.ids.friday.color = self.active_color if self.friday_active else self.inactive_color
        self.ids.saturday.color = self.active_color if self.saturday_active else self.inactive_color

    def toggle_enabled(self, is_active):
        """Toggle the enabled state of the alarm and update the AlarmItem instance."""
        self.alarm_enabled = is_active
        if self.alarm_item is not None:  # Check if alarm_item is properly assigned
            self.alarm_item.enabled = is_active
            if hasattr(self.alarm_item, 'refresh_callback'):
                self.alarm_item.refresh_callback()  # Refresh data if callback is set
        else:
            print("Warning: alarm_item is None in toggle_enabled")


class AlarmScreen(Screen):
    def on_enter(self):
        self.AlarmList = []

        self.load_alarm_list()
        self.load_widgets()

        
    def save_and_reload(self):
        self.save_alarm_list()
        self.load_widgets()

    def load_widgets(self):
        self.ids.alarm_list.data = [item.to_widget() for item in self.AlarmList]

    def open_editor(self, alarm_item):
        self.popup = EditorPopup(alarm_item, refresh_callback=self.save_and_reload)
        self.popup.open()
    
    def add_alarm(self):
        pass

    def load_alarm_list(self):
    # Define the path to the alarms.json file
        file_path = "data/alarms.json"  # Adjust this path if necessary
        
        # Check if the file exists before attempting to read it
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                # Load the JSON data from the file
                alarm_data = json.load(file)

                # Loop through the alarm data and convert each item into an AlarmItem
                for alarm_json in alarm_data:
                    alarm = AlarmItem.from_json(json.dumps(alarm_json), self.save_alarm_list)  # Convert dict to JSON string for from_json
                    self.AlarmList.append(alarm)
        else:
            print(f"Error: The file {file_path} does not exist.")

    def save_alarm_list(self):
        """Save the current alarm list back to alarms.json."""
        file_path = "data/alarms.json"  # Ensure this matches the path used in load_alarm_list

        # Convert AlarmList to a list of dictionaries
        alarm_data = []
        for alarm in self.AlarmList:
            alarm_dict = {
                "name": alarm.name,
                "time": alarm.time,
                "enabled": alarm.enabled,
                "media_path": alarm.media_path,
                "repeat": alarm.repeat,
                "volume": alarm.volume_gradient,
                "light": alarm.light_gradient,
                "days": "".join("1" if day else "0" for day in alarm.days)  # Convert days list back to string
            }
            alarm_data.append(alarm_dict)

        # Write the data to alarms.json
        try:
            with open(file_path, "w") as file:
                json.dump(alarm_data, file, indent=4)  # Use indent for a readable JSON file
            print(f"Successfully saved alarms to {file_path}.")
        except Exception as e:
            print(f"Error saving alarms: {e}")

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

    active_color = (1, 1, 1, 1)  # Example color for active state (white)
    inactive_color = (0.5, 0.5, 0.5, 1)  # Example color for inactive state (gray)

    # Properties to track each day’s active state
    sunday_active = BooleanProperty(False)
    monday_active = BooleanProperty(False)
    tuesday_active = BooleanProperty(False)
    wednesday_active = BooleanProperty(False)
    thursday_active = BooleanProperty(False)
    friday_active = BooleanProperty(False)
    saturday_active = BooleanProperty(False)

    selected_digit = StringProperty('hour_ten')  # Default selection

    def __init__(self, alarm_item, refresh_callback, **kwargs):
        super().__init__(**kwargs)
        self.alarm_item = alarm_item
        self.refresh_callback = refresh_callback
        self.title = "Editing Alarm: " + alarm_item.name
        self.update_inputs()
        self.load_media_list()
        self.load_time()
        
    def update_media_label(self, selected_text):
        """Updates the media_selected_label with the selected media file name."""
        self.ids.media_selected_label.text = selected_text  # Update the label text
        print(f"Media selected: {selected_text}")  # Optional debug print to check selection

    def load_media_list(self):
        # Example: Mock list of media file names
        media_files = ["Alarm1.mp3", "Alarm2.mp3", "Nature.mp3", "Ocean.mp3"]

        # Populate the RecycleView with the media files
        self.ids.media_list.data = [{'text': file} for file in media_files]

    def select_digit(self, digit_id):
        self.selected_digit = digit_id
        self.update_highlight()

    def update_highlight(self):
        for digit in ['hour_ten', 'hour_one', 'minute_ten', 'minute_one']:
            button = self.ids[digit]
            button.color = self.active_color if digit == self.selected_digit else self.inactive_color

    def change_digit(self, increment=True):
        digit_id = self.selected_digit
        button = self.ids[digit_id]
        value = int(button.text)

        if digit_id.startswith('hour'):
            max_value = 2 if digit_id == 'hour_ten' else (3 if self.ids.hour_ten.text == '2' else 9)
        else:
            max_value = 5 if digit_id == 'minute_ten' else 9

        if increment:
            value = (value + 1) % (max_value + 1)
        else:
            value = (value - 1) % (max_value + 1)

        button.text = str(value)

    def toggle_day(self, day_button_id):
        """Toggle the active state of a day button based on its ID."""
        # Access the button using the ID
        if day_button_id == 'sunday_button':
            self.sunday_active = not self.sunday_active
        elif day_button_id == 'monday_button':
            self.monday_active = not self.monday_active
        elif day_button_id == 'tuesday_button':
            self.tuesday_active = not self.tuesday_active
        elif day_button_id == 'wednesday_button':
            self.wednesday_active = not self.wednesday_active
        elif day_button_id == 'thursday_button':
            self.thursday_active = not self.thursday_active
        elif day_button_id == 'friday_button':
            self.friday_active = not self.friday_active
        elif day_button_id == 'saturday_button':
            self.saturday_active = not self.saturday_active

        # Force a re-render to apply color changes
        self.ids[day_button_id].color = (
            self.active_color if getattr(self, f"{day_button_id.split('_')[0]}_active") else self.inactive_color
        )

    def update_time(self):
        hours = int(self.ids.hour_ten.text) * 10 + int(self.ids.hour_one.text)
        minutes = int(self.ids.minute_ten.text) * 10 + int(self.ids.minute_one.text)
        self.alarm_item.time = f"{hours:02}:{minutes:02}"

    def load_time(self):
        hours, minutes = map(int, self.alarm_item.time.split(':'))
        self.ids.hour_ten.text, self.ids.hour_one.text = str(hours // 10), str(hours % 10)
        self.ids.minute_ten.text, self.ids.minute_one.text = str(minutes // 10), str(minutes % 10)


    def update_inputs(self):
        self.ids.volume_switch.active = self.alarm_item.volume_gradient
        self.ids.light_switch.active = self.alarm_item.light_gradient
        self.ids.repeat_switch.active = self.alarm_item.repeat
        """Initialize button states based on `AlarmItem.days`."""
        # Set each button's active state from `self.alarm_item.days`
        self.sunday_active = self.alarm_item.days[0]
        self.monday_active = self.alarm_item.days[1]
        self.tuesday_active = self.alarm_item.days[2]
        self.wednesday_active = self.alarm_item.days[3]
        self.thursday_active = self.alarm_item.days[4]
        self.friday_active = self.alarm_item.days[5]
        self.saturday_active = self.alarm_item.days[6]

        # Set button colors based on active states
        self.ids.sunday_button.color = self.active_color if self.sunday_active else self.inactive_color
        self.ids.monday_button.color = self.active_color if self.monday_active else self.inactive_color
        self.ids.tuesday_button.color = self.active_color if self.tuesday_active else self.inactive_color
        self.ids.wednesday_button.color = self.active_color if self.wednesday_active else self.inactive_color
        self.ids.thursday_button.color = self.active_color if self.thursday_active else self.inactive_color
        self.ids.friday_button.color = self.active_color if self.friday_active else self.inactive_color
        self.ids.saturday_button.color = self.active_color if self.saturday_active else self.inactive_color

    def save_changes(self):
        """Save the changes made in the editor and refresh the alarm list."""
        # Update the alarm item's properties based on the current inputs
        self.alarm_item.volume_gradient = self.ids.volume_switch.active
        self.alarm_item.light_gradient = self.ids.light_switch.active
        self.alarm_item.repeat = self.ids.repeat_switch.active
        self.alarm_item.media_path = self.ids.media_selected_label.text
        self.alarm_item.days = [
            self.sunday_active, self.monday_active, self.tuesday_active,
            self.wednesday_active, self.thursday_active, self.friday_active,
            self.saturday_active
        ]
        self.update_time()

        # Use the refresh callback to update widgets and save alarms
        if self.refresh_callback:
            self.refresh_callback()  # Refresh the alarm list UI

        # Close the editor popup
        self.dismiss()