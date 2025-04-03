# Internet-Radio
A simple internet radio for your Raspberry Pi. The entire radio assembly is of course made up of the RPi microcomputer (the program is not demanding, the recording version should be enough for it to run). You also need a 2x20 line LCD display (HD44780) with an I2C converter. Finally, you need 4 buttons.

The following radios are currently added to the configuration: <b>Kiss rádio</b>, <b>Evropa 2</b>, <b>Rock rádio</b>, <b>Rádio Beat</b>, <b>Dance rádio</b>, <b>Fajn Rádio</b>, <b>Hitrádio Černá Hora</b>, <b>Hitrádio Osmdesátka</b>, <b>ČRo Radiožurnál</b>, <b>Frekvence 1</b> and as a bonus there is also a stream from radio traffic at BRNO airport.

The above radios are of course fully configurable and can be changed to your own internet streams. The full configuration guide is in the [Config](#config) section.

## Install

```console
cd /opt
sudo apt update && sudo apt upgrade -y
sudo apt install git vlc python3-pip python3-smbus -y
sudo apt install i2c-tools libvlc-dev libvlccore-dev -y
sudo git clone https://github.com/ondrahladik/Internet-Radio.git
sudo pip3 install -r requirements.txt
cd Internet-Radio
```
After installation, you will need to enable  I²C.
```console
sudo raspi-config
```
Interface Options -> I2C -> YES 

You can check whether your I²C LCD is connected and installed correctly using:
```console
sudo i2cdetect -y 1
```
The output should contain the address of your device.

## Config

```console
sudo nano config.py
```
The program is configured using the config.py file where you can customize some settings, but this is not necessary for functionality after installation.   

A complete description of the configuration is on the [Wiki](https://github.com/ondrahladik/Internet-Radio/wiki) page. 

Before you start configuring the service, you can check if you have all the packages and dependencies installed by running the program manually.
```console
sudo python3 main.py
```
## Service config

Creating a service file:
```console
sudo nano /etc/systemd/system/Internet-Radio.service
```
Put these lines in the file:
```console
[Unit]
Description=Internet-Radio
After=network.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/python3 /opt/Internet-Radio/main.py
WorkingDirectory=/opt/Internet-Radio
StandardOutput=append:/var/log/Internet-Radio.log
StandardError=append:/var/log/Internet-Radio_error.log
Restart=always

[Install]
WantedBy=multi-user.target
```
Starting the service:
```console
sudo systemctl daemon-reload
sudo systemctl enable Internet-Radio
sudo systemctl start Internet-Radio
```
Adding permissions for log files:
```console
sudo chmod 666 /var/log/Internet-Radio.log
sudo chmod 666 /var/log/Internet-Radio_error.log
```
Service management:
```console
sudo systemctl start Internet-Radio # Starting the service
sudo systemctl restart Internet-Radio # Restart the service
sudo systemctl stop Internet-Radio # Stop the service
sudo systemctl status Internet-Radio # Service status
tail -f /var/log/Internet-Radio.log # Tracking logs
```