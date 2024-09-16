#!/bin/bash

USER_SERVICE_DIR=/etc/systemd/system
SERVICE_FILE=oled.service

mkdir $USER_SERVICE_DIR

echo "Create service file : $SERVICE_FILE"
printf "\
[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/2024-players_code/service/oled/oled.py
User=pi
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
" > $USER_SERVICE_DIR/$SERVICE_FILE

sudo chmod +x $USER_SERVICE_DIR/$SERVICE_FILE

echo "Start service : $SERVICE_FILE"
sudo systemctl daemon-reload
sudo systemctl reenable $SERVICE_FILE
sudo systemctl restart $SERVICE_FILE
sudo systemctl status $SERVICE_FILE

