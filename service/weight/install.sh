#!/bin/bash

USER_SERVICE_DIR=/etc/systemd/system
SERVICE_FILE=weight.service

mkdir $USER_SERVICE_DIR

echo "Create service file : $SERVICE_FILE"
printf "\
[Unit]
After=network.target sound.target

[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/2024-players_code/service/weight/weight.py
User=pi
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
" > $USER_SERVICE_DIR/$SERVICE_FILE

chmod +x $USER_SERVICE_DIR/$SERVICE_FILE

echo "Start service : $SERVICE_FILE"
systemctl daemon-reload
systemctl reenable $SERVICE_FILE
systemctl restart $SERVICE_FILE
systemctl status $SERVICE_FILE
