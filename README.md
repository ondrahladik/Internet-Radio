# Internet-Radio

## Install

```console
cd /opt
sudo apt update && sudo apt upgrade -y
sudo apt install git vlc python3-pip python3-smbus -y
sudo apt install i2c-tools libvlc-dev libvlccore-dev -y
sudo apt install git vlc python3-pip python3-smbus libvlc-dev libvlccore-dev i2c-tools -y
sudo git clone https://github.com/ondrahladik/Internet-Radio.git
cd Internet-Radio
sudo pip3 install -r requirements.txt
```