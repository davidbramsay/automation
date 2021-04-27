
for importerror from vlc (inspect has no attribute signature)
install funcsigs and replace inspect  with funcsigs at import

VLC doesn't like repeat=-1, make sure to use 999999

we need to patch OLA first, though it will
startup when we start up the pi WITH saved configs.  So
you can just go to OLAD (127.0.0.1:9090) and enable
a USB-FTDI driven universe 1.

ola_dev_info
ola_patch
start ola : olad

#get device number with bash
ola_dev_info | grep KMtronic | grep Device | sed 's@^[^0-9]*\([0-9]\+\).*@\1@'

#get device port with bash
ola_dev_info | grep KMtronic | grep port | sed 's@^[^0-9]*\([0-9]\+\).*@\1@'

ola_patch -d <device-num> -p <port-num> -u 1


SYSTEMD--
copy the service file to /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/automationservice.service
sudo systemctl daemon-reload
sudo systemctl enable automationserver.service

debug with
journalctl -b
