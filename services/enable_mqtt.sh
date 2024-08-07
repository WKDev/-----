#!/bin/bash

SERVICE_NAME=mqtt_gpio_controller
SERVICE_FILE=/etc/systemd/system/${SERVICE_NAME}.service
SCRIPT_PATH=/usr/local/bin/mqtt_gpio_controller.py

# 서비스 중지 및 비활성화
sudo systemctl stop $SERVICE_NAME.service
sudo systemctl disable $SERVICE_NAME.service

# systemd 유닛 파일 삭제
sudo rm $SERVICE_FILE

# Python 스크립트 삭제
sudo rm $SCRIPT_PATH

# 유닛 파일 리로드
sudo systemctl daemon-reload

echo "Service $SERVICE_NAME uninstalled."
