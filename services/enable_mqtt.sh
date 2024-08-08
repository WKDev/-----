#!/bin/bash

SERVICE_NAME=mqtt_gpio_controller
SCRIPT_PATH=/usr/local/bin/mqtt_gpio_controller
SERVICE_FILE=/etc/systemd/system/${SERVICE_NAME}.service

# Python 스크립트를 /usr/local/bin에 복사
sudo mkdir -p $SCRIPT_PATH
sudo cp -r ../ $SCRIPT_PATH
sudo chmod +x $SCRIPT_PATH/main.py

# systemd 서비스 유닛 파일 작성
cat <<EOL | sudo tee $SERVICE_FILE
[Unit]
Description=SID MQTT GPIO Controller Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/$SERVICE_NAME/main.py
WorkingDirectory=/usr/local/bin/$SERVICE_NAME
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root
Environment=PYTHONUNBUFFERED=1
Environment=HOME=/usr/local/bin/$SERVICE_NAME
Environment=PATH=/usr/local/bin:/usr/bin:/bin


[Install]
WantedBy=multi-user.target
EOL

# 유닛 파일 리로드 및 서비스 시작
sudo systemctl daemon-reload
sudo systemctl start $SERVICE_NAME.service
sudo systemctl enable $SERVICE_NAME.service

echo "Service $SERVICE_NAME installed and started."
