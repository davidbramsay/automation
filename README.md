### start olad

```
sudo kextunload /System/Library/Extensions/FTDIUSBSerialDriver.kext
olad -l 2
```

### start flic server

```
python flic_server.py
```

### start qlab (GUI)

qlab will talk to the main script with MIDI-- midi goes to qlab
automatically through the qlab virtual midi port, qlab outputs on
Apple's IAC bus 1 (or whatever the first open midi port is).

### start main cue script

it uses ARP to identify switches by their MAC address, so needs
to be run with sudo

```
sudo python bnw_midi_controller.py
```


flic calls flic_client.py when triggered, which updates state using flic_server
and sends midi commands to QLab.  bnw_midi_controller handles midi commands
from QLab to dmx lights and outlets.
