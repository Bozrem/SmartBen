from flask import Flask, request, jsonify
import subprocess, re, os

app = Flask(__name__)

def get_connected_bluetooth_device():
    try:
        cmd = ["dbus-send", "--system", "--print-reply", "--dest=org.bluez", "/", "org.freedesktop.DBus.ObjectManager.GetManagedObjects"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout

        device_pattern = re.compile(r'(/org/bluez/hci0/dev_([A-F0-9_]+))')
        devices = device_pattern.findall(output)
        
        for device_path, mac in devices:
            device_mac = mac.replace('_', ':')
            cmd = ["dbus-send", "--system", "--print-reply", "--dest=org.bluez", device_path, "org.freedesktop.DBus.Properties.Get", "string:org.bluez.MediaControl1", "string:Player"]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if "No such interface" not in result.stdout and "Error" not in result.stderr:
                return device_mac, device_path

        return None, None

    except subprocess.CalledProcessError as e:
        print(f"Error checking Bluetooth devices: {e}")
        return None, None

def get_bluetooth_player_info(device_path):
    try:
        # Append /player0 to the device path to access player info
        player_path = f"{device_path}/player0"
        
        # Query the player properties
        cmd = [
            "dbus-send", "--system", "--print-reply", "--dest=org.bluez",
            player_path, "org.freedesktop.DBus.Properties.GetAll", "string:org.bluez.MediaPlayer1"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout

        info = {}
        current_key = None
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("string "):
                current_key = line.split('"')[1]
            elif line.startswith("variant") and current_key:
                value = line.split("variant")[1].strip().strip('"')
                # Clean the value by removing type prefixes and extra quotes
                if value.startswith("string "):
                    value = value[len("string "):].strip('"')
                elif value.startswith("uint32 "):
                    value = value[len("uint32 "):].strip('"')
                elif value.startswith("object path "):
                    value = value[len("object path "):].strip('"')
                info[current_key] = value
                current_key = None

        return info
    except subprocess.CalledProcessError as e:
        print(f"Error getting player info: {e}")
        return None


        return info
    except subprocess.CalledProcessError as e:
        print(f"Error getting player info: {e}")
        return None

def bluetooth_pause(path):
    cmd = ["dbus-send", "--system", "--print-reply", "--dest=org.bluez", f"{path}", "org.bluez.MediaControl1.Pause"]
    try:
        subprocess.run(cmd, check=True)
        return jsonify({'status': 'success', 'toggled_from': 'playing'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Error toggling media player: {e}'})
    
def bluetooth_play(path):
    cmd = ["dbus-send", "--system", "--print-reply", "--dest=org.bluez", f"{path}", "org.bluez.MediaControl1.Play"]
    try:
        subprocess.run(cmd, check=True)
        return jsonify({'status': 'success', 'toggled_from': 'paused'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Error toggling media player: {e}'})    

@app.route('/api/media/toggle', methods=['POST'])
def toggle_bluetooth_media():
    device_mac, path = get_connected_bluetooth_device()
    if path:  # BT mode
        player_info = get_bluetooth_player_info(path)
        if player_info:
            status = player_info.get('Status', '').strip().lower()
            if 'playing' in status: 
                return bluetooth_pause(path)
            elif 'paused' in status:
                return bluetooth_play(path)
            else:
                return jsonify({'status': 'error', 'message': f'Unknown player status: {status}'})
        else:
            return jsonify({'status': 'error', 'message': 'Unable to get player info'})
    else:
        return jsonify({'status': 'error', 'message': 'No Bluetooth device is connected or supports MediaControl1.'})

@app.route('/api/media/start', methods=['POST'])
def play_local():
    file_path = request.json.get('path')
    if not file_path:
        return jsonify({'status': 'error', 'message': 'No file path provided'}), 400
    try:
        subprocess.run(['mpg123', file_path], check=True)
        return jsonify({'status': 'playing', 'file': file_path})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Error playing local file: {e}'})

@app.route('/api/media/stop', methods=['POST'])
def stop_local():
    try:
        subprocess.run(['pkill', 'mpg123'], check=True)
        return jsonify({'status': 'stopped'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Error stopping local file: {e}'})

@app.route('/api/media/next', methods=['POST'])
def next_track():
    device_mac, path = get_connected_bluetooth_device()
    if path:
        cmd = ["dbus-send", "--system", "--print-reply", "--dest=org.bluez", f"{path}", "org.bluez.MediaControl1.Next"]
        try:
            subprocess.run(cmd, check=True)
            return jsonify({'status': 'next track'})
        except subprocess.CalledProcessError as e:
            return jsonify({'status': 'error', 'message': f'Error skipping to next track: {e}'})
    else:
        return jsonify({'status': 'error', 'message': 'No Bluetooth device is connected or supports MediaControl1.'})

@app.route('/api/media/previous', methods=['POST'])
def previous_track():
    device_mac, path = get_connected_bluetooth_device()
    if path:
        cmd = ["dbus-send", "--system", "--print-reply", "--dest=org.bluez", f"{path}", "org.bluez.MediaControl1.Previous"]
        try:
            subprocess.run(cmd, check=True)
            return jsonify({'status': 'previous track'})
        except subprocess.CalledProcessError as e:
            return jsonify({'status': 'error', 'message': f'Error skipping to previous track: {e}'})
    else:
        return jsonify({'status': 'error', 'message': 'No Bluetooth device is connected or supports MediaControl1.'})

@app.route('/api/media/playback_info', methods=['GET'])
def playback_info():
    device_mac, path = get_connected_bluetooth_device()
    if path:
        player_info = get_bluetooth_player_info(path)
        if player_info:
            return jsonify({'player_info': player_info})
        else:
            return jsonify({'status': 'error', 'message': 'Unable to get player info'})
    else:
        return jsonify({'status': 'error', 'message': 'No Bluetooth device is connected or supports MediaPlayer1'})

@app.route('/api/media/bluetooth_toggle', methods=['POST'])
def toggle_bluetooth():
    try:
        result = subprocess.run(['bluetoothctl', 'show'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        if "Powered: yes" in output:
            subprocess.run(['bluetoothctl', 'power', 'off'], check=True)
            return jsonify({'status': 'Bluetooth turned off'})
        else:
            subprocess.run(['bluetoothctl', 'power', 'on'], check=True)
            subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '100%'], check=True)
            return jsonify({'status': 'Bluetooth turned on'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Error toggling Bluetooth: {e}'})
    
def enable_bluetooth_pairing_mode():
    try:
        # Stop any existing instances of the agent script, ignoring errors if no process is found
        subprocess.run(['pkill', '-f', 'bluetooth_agent.sh'], check=False)
        
        # Start the agent script in the background
        script_path = os.path.abspath("bluetooth_agent.sh")
        subprocess.Popen([script_path])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error enabling Bluetooth pairing mode: {e}")
        return False

@app.route('/api/bluetooth/pairing_mode', methods=['POST'])
def bluetooth_pairing_mode():
    success = enable_bluetooth_pairing_mode()
    if success:
        return jsonify({'status': 'success', 'message': 'Bluetooth is now in pairing mode'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to enable Bluetooth pairing mode'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
