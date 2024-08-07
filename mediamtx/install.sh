# update dependencies
sudo apt update
sudo apt upgrade
sudo apt install screen -y
sudo apt install -y ffmpeg
sudo apt install -y net-tools
sudo apt install python3-pip -y

echo "=================================="
echo "installing mediamtx"
echo "=================================="

# Install mediamtx
wget https://github.com/bluenviron/mediamtx/releases/download/v1.8.5/mediamtx_v1.8.5_linux_arm64v8.tar.gz
rm -rf mediamtx.yml
tar -xvf mediamtx_v1.8.5_linux_arm64v8.tar.gz
sudo mv mediamtx /usr/local/bin/
sudo mv mediamtx_temp.yml /usr/local/etc/mediamtx.yml
rm -rf mediamtx_v1.8.5_linux_arm64v8.tar.gz


sudo tee /etc/systemd/system/mediamtx.service >/dev/null << EOF
[Unit]
Wants=network.target
[Service]
ExecStart=/usr/local/bin/mediamtx /usr/local/etc/mediamtx.yml
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable mediamtx
sudo systemctl start mediamtx

echo "mediamtx installed."