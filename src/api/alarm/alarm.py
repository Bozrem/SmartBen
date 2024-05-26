import json
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, jsonify

class Alarm:
    def __init__(self, name, timestamp, state, media_path):
        self.name = name
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        self.state = state
        self.media_path = media_path

    @staticmethod
    def decode(json_data):
        print("decode called")
        return Alarm(json_data['name'], json_data['timestamp'], json_data['state'], json_data['media_path'])
    
    def encode(self):
        print("encode called")
        return {
            'name': self.name,
            'timestamp': self.timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
            'state': self.state,
            'media_path': self.media_path
        }

    def update_next_trigger_time(self):
        # Placeholder: Update timestamp for repeating alarms
        pass

    def is_active(self):
        return self.state == 'enabled'

class AlarmManager:
    def __init__(self):
        self.current_alarm = None
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def get_alarms(self):
        print("get called")
        try:
            with open('/home/bozrem/Projects/SmartBen/src/api/alarm/alarms.json', 'r') as f:
                data = json.load(f)
            alarms = [Alarm.decode(alarm) for alarm in data]
            return alarms
        except (IOError, ValueError) as e:
            print(f"Error reading alarms: {e}")
            return []

    def save_alarms(self, alarms):
        print("save called")
        try:
            with open('/home/bozrem/Projects/SmartBen/src/api/alarm/alarms.json', 'w') as f:
                json.dump([alarm.encode() for alarm in alarms], f)
            self.schedule()
        except IOError as e:
            print(f"Error saving alarms: {e}")

    def trigger_alarm(self, alarm):
        print("trigger called")
        self.current_alarm = alarm
        if alarm.is_active():
            # Placeholder: Handle triggering the alarm (e.g., play media, update UI)
            print(f"Triggering alarm: {alarm.name}")
        

    def dismiss_alarm(self):
        if self.current_alarm:
            # Placeholder: Handle dismiss logic
            print(f"Dismissing alarm: {self.current_alarm.name}")
            self.current_alarm = None
            self.schedule()

    def snooze_alarm(self):
        if self.current_alarm:
            now = datetime.now()
            self.current_alarm.timestamp = now + timedelta(minutes=5)
            print(f"Snoozing alarm: {self.current_alarm.name} for 5 minutes from now")
            alarms = self.get_alarms()
            for alarm in alarms:
                if alarm.name == self.current_alarm.name:
                    alarm.timestamp = self.current_alarm.timestamp
            self.save_alarms(alarms)
            self.current_alarm = None

    def schedule(self):
        print("Schedule called")
        alarms = self.get_alarms()
        now = datetime.now()
        if alarms:
            next_alarm = min((alarm for alarm in alarms if alarm.is_active() and alarm.timestamp > now), key=lambda a: a.timestamp, default=None)
            if next_alarm:
                self.scheduler.remove_all_jobs()
                self.scheduler.add_job(self.trigger_alarm, 'date', run_date=next_alarm.timestamp, args=[next_alarm])
                print(f"Scheduled next alarm: {next_alarm.name} at {next_alarm.timestamp}")

app = Flask(__name__)
alarm_manager = AlarmManager()

@app.route('/alarms', methods=['GET'])
def get_alarms_api():
    alarms = alarm_manager.get_alarms()
    return jsonify([alarm.encode() for alarm in alarms])

@app.route('/alarms', methods=['POST'])
def save_alarms_api():
    alarms_data = request.json
    alarms = [Alarm.decode(alarm) for alarm in alarms_data]
    alarm_manager.save_alarms(alarms)
    return 'Alarms updated', 200

@app.route('/alarms/dismiss', methods=['POST'])
def dismiss_alarm_api():
    alarm_manager.dismiss_alarm()
    return 'Alarm dismissed', 200

@app.route('/alarms/snooze', methods=['POST'])
def snooze_alarm_api():
    alarm_manager.snooze_alarm()
    return 'Alarm snoozed', 200

if __name__ == '__main__':
    app.run()

# TODO
# Feat. Repeatable Alarms
# Fix. Limit Snoozes
# Feat. Actual Trigger functionality with Media API
# Feat. Improve logging output
# Feat. Add endpoint to check for an active alarm