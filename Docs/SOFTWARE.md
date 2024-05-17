# Software
Most of my time has gone into designing the system architecture to make it easy to repair, upgrade, and expand

## APIs
The biggest way that I'm modularizing the design is to write the different components as their own seperate Python scripts running as services that interact through HTTP requests

### Media API
The Media API manages anything to do with what media is playing on the system. This could be media from alarms going off to media from a Bluetooth connection.
#### Incoming requests:
Commands API from app commands to pause/play, skip, etc.\
Alarm API to play media for an alarm going off\
Buttons service for physical button presses for media control and Bluetooth enabling\
#### Outgoing requests:
Web Interface to update the media widget with what is currently playing

### Commands API
The Commands API manages all incoming requests from the phone app over Bluetooth
#### Incoming requests:
None
#### Outgoing requests:
Media API to update media status\
Alarm API to set, cancel, enable, or delete alarms

### Alarm API
The Alarm API manages all alarms on the system. It keeps track of the status of each one and sends signals to other APIs when one needs to go off
#### Incoming requests:
Commands API from app commands to set, cancel, enable, or delete alarms\
Buttons service from physical button presses to dismiss or snooze alarms going off\
#### Outgoing requests:
Web Interface to update the alarms widget on upcoming and current alarms

## Web Interface
Upon boot, a script (~/.xinitrc) enables both hosting the local web server, and launching Chromium to Kiosk mode to display it. The interface uses the React framework to render individual independent widgets on a single dashboard\
This functionality is a work in progress, as I've never dealt with web development before

## Services
Either periodic or constantly running
### Button Service
Monitors the GPIO pins for button presses. Handles them and sends requests to the appropriate API. More information on the button configuration can be found in [the Hardware Documentation](HARDWARE.md)
#### Outgoing Requests:
Media API for media playback control and Bluetooth mode toggle
Alarm API to snooze or dismiss

## File System
I will get this into GitHub eventually, but here is the file system layout


/home/bozrem/\
├── api/\
│   ├── media_api.py\
│   ├── alarm_api.py\
│   └── commands_api.py\
├── web/\
│   ├── public/\
│   │   ├── css/\
│   │   │   └── style.css\
│   │   ├── js/\
│   │   │   └── main.js\
│   │   └── index.html\
│   ├── server.py\
│   ├── templates/\
│   │   └── index.html\
│   └── widgets/\
│       ├── TimeWidget.js\
│       ├── AlarmWidget.js\
│       ├── WeatherWidget.js\
│       ├── CalendarWidget.js\
│       └── MicStatusWidget.js\
├── services/\
│   ├── button_service.py\
│   └── wakeword.py\
└── config/\
    └── config.json

/etc/systemd/system/\
├── dashboard.service

~/\
└── .xinitrc
