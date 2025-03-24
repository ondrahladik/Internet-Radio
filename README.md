# Internet-Radio

The following radios are currently added to the configuration: <b>Kiss rádio</b>, <b>Evropa 2</b>, <b>Rock rádio</b>, <b>Rádio Beat</b>, <b>Dance rádio</b>, <b>Fajn Rádio</b>, <b>Hitrádio Černá Hora</b>, <b>Hitrádio Osmdesátka</b>, <b>ČRo Radiožurnál</b>, <b>Frekvence 1</b> and as a bonus there is also a stream from radio traffic at BRNO airport.

## Install

```console
cd /opt
sudo apt update && sudo apt upgrade -y
sudo apt install git vlc python3-pip python3-smbus -y
sudo apt install i2c-tools libvlc-dev libvlccore-dev -y
sudo apt install git vlc python3-pip python3-smbus libvlc-dev libvlccore-dev i2c-tools -y
sudo git clone https://github.com/ondrahladik/Internet-Radio.git
sudo pip3 install -r requirements.txt
cd Internet-Radio
```
After installation, you will need to enable  I²C.
```console
sudo raspi-config
```
Interface Options -> I2C -> YES 

## Config

```console
sudo nano config.py
```
The program is configured using the config.py file where you can customize some settings, but this is not necessary for functionality after installation.  

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

```
Starting the service:
```console
sudo systemctl daemon-reload
sudo systemctl enable Internet-Radio
sudo systemctl start Internet-Radio
```
Service management:
```console
sudo systemctl start Internet-Radio # Starting the service
sudo systemctl restart Internet-Radio # Restart the service
sudo systemctl stop Internet-Radio # Stop the service
sudo systemctl status Internet-Radio # Service status
tail -f /var/log/Internet-Radio.log # Tracking logs
```