#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
USER_SERVICE_DIR=/etc/systemd/system
SERVICE_NAME=adc

mkdir $USER_SERVICE_DIR

echo "Create service file : $SERVICE_NAME.service"
printf "\
[Timer]
OnBootSec=3s

[Service]
Type=simple
ExecStart=/usr/bin/python $SCRIPT_DIR/$SERVICE_NAME.py --service
User=pi
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
" > $USER_SERVICE_DIR/$SERVICE_NAME.service

chmod +x $USER_SERVICE_DIR/$SERVICE_NAME.service

echo "Start service : $SERVICE_NAME.service"
systemctl daemon-reload
systemctl reenable $SERVICE_NAME.service
systemctl restart $SERVICE_NAME.service

