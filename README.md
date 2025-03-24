# Internet-Radio

The following radios are currently added to the configuration: Kiss rádio, Evropa 2, Rock rádio, Rádio Beat, Dance rádio, Fajn Rádio, Hitrádio Černá Hora, Hitrádio Osmdesátka, ČRo Radiožurnál, Frekvence 1 and as a bonus there is also a stream from radio traffic at BRNO airport.

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