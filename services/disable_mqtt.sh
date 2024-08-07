#!/bin/bash

SERVICE_NAME=mqtt_gpio_controller
SCRIPT_PATH=/usr/local/bin/mqtt_gpio_controller.py
SERVICE_FILE=/etc/systemd/system/${SERVICE_NAME}.service

# Python 스크립트를 /usr/local/bin에 복사
sudo cp mqtt_gpio_controller.py $SCRIPT_PATH
sudo chmod +x $SCRIPT_PATH

# systemd 서비스 유닛 파일 작성
cat <<EOL | sudo tee $SERVICE_FILE
[Unit]
Description=MQTT GPIO Controller Service
After=network.target

[Service]
ExecStart=$SCRIPT_PATH
WorkingDirectory=/usr/local/bin
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi  # 사용자를 실제 사용자로 변경하십시오
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

# 유닛 파일 리로드 및 서비스 시작
sudo systemctl daemon-reload
sudo systemctl start $SERVICE_NAME.service
sudo systemctl enable $SERVICE_NAME.service

echo "Service $SERVICE_NAME installed and started."
