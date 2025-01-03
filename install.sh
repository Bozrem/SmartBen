#!/bin/sh

: ' Project TODO
Set a path to the correct spot
Make code use the path

'

echo "Aquiring newest versions"
apt -y update
apt -y upgrade

echo "Aquiring media control packages"
apt install -y pulseaudio pulseaudio-module-bluetooth bluez-tools mpg123 bluetooth blueman

echo "Aquiring python packages"
apt install -y python3-flask python3-apscheduler python3-bluez

echo "Done."