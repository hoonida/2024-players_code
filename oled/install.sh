#!/bin/bash

USER_SERVICE_DIR=~/.config/systemd/user
SERVICE_FILE=oled.service

mkdir $USER_SERVICE_DIR

echo "Create service file : $SERVICE_FILE"
printf "\
[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/2024-players_code/oled/oled.py
Restart=on-abort
ExecStartPre=-/bin/sleep 5

[Install]
WantedBy=default.target
" > $USER_SERVICE_DIR/$SERVICE_FILE

chmod +x $USER_SERVICE_DIR/$SERVICE_FILE

echo "Start service : $SERVICE_FILE"
systemctl --user daemon-reload
systemctl --user reenable $SERVICE_FILE
systemctl --user restart $SERVICE_FILE
systemctl --user status $SERVICE_FILE

