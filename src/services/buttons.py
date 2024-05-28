from gpiozero import Button
from signal import pause
from time import time
import requests

# Define the GPIO pins for the buttons
button1 = Button(17)
button2 = Button(27)
button3 = Button(22)

# Define dictionaries to store the press times
press_times = {
    17: 0,
    27: 0,
    22: 0
}

# Define functions to be called for clicks and holds
def button1_click(duration):
    print(f"Button 1 (GPIO 17) click ({duration} seconds)")
    response = requests.get('http://localhost:5000/api/alarms/active')
    if response.json().get('active'):
        requests.post('http://localhost:5000/api/alarms/dismiss')
    else:
        requests.post('http://localhost:5001/api/media/toggle')

def button1_hold(duration):
    print(f"Button 1 (GPIO 17) hold ({duration} seconds)")
    # No current functionality for hold, placeholder

def button2_click(duration):
    print(f"Button 2 (GPIO 27) click ({duration} seconds)")
    requests.post('http://localhost:5001/api/media/bluetooth_toggle')

def button2_hold(duration):
    print(f"Button 2 (GPIO 27) hold ({duration} seconds)")
    requests.post('http://localhost:5001/api/bluetooth/pairing_mode')

def button3_click(duration):
    print(f"Button 3 (GPIO 22) click ({duration} seconds)")
    response = requests.get('http://localhost:5000/api/alarms/active')
    if response.json().get('active'):
        requests.post('http://localhost:5000/api/alarms/snooze')
    else:
        requests.post('http://localhost:5001/api/media/next')

def button3_hold(duration):
    print(f"Button 3 (GPIO 22) hold ({duration} seconds)")
    # No current functionality for hold, placeholder

# Function to handle button press
def on_press(pin):
    press_times[pin] = time()

# Function to handle button release
def on_release(pin, click_callback, hold_callback):
    press_duration = time() - press_times[pin]
    if 0.03 < press_duration < 2.0:
        click_callback(press_duration)
    elif press_duration > 0.03:
        hold_callback(press_duration)

# Attach the functions to the button events
button1.when_pressed = lambda: on_press(17)
button1.when_released = lambda: on_release(17, button1_click, button1_hold)

button2.when_pressed = lambda: on_press(27)
button2.when_released = lambda: on_release(27, button2_click, button2_hold)

button3.when_pressed = lambda: on_press(22)
button3.when_released = lambda: on_release(22, button3_click, button3_hold)

# Keep the script running to listen for button presses
pause()
