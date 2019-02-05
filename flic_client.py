#!/Users/davidramsay/.virtualenvs/audio-perform/bin/python

#must have flic_state_server.py running in the background
PORT = 12345
import rpyc
import rtmidi

#connect and get current click and any other state we want to store
conn = rpyc.connect("localhost", PORT)
state_server = conn.root
click_num = state_server.i()

#listens for flic, if it does, dispatches a MIDI message.

#we only have 3 cues-- start video, panic, end panic
#panic and end panic must have the same midi signature

#these will send Note ON, 0, 0 to start the video
#these will send Note ON, 1, 1 to start/end panic
#these will send Note ON, 1, 2 also to end panic

click_iteration = click_num % 3

midi_out = rtmidi.MidiOut()
ports_out = midi_out.get_ports()
print ports_out

if 'QLab' in ports_out:
    print 'using QLab for output'
    midi_out.open_port(ports_out.index('QLab'))
else:
    print 'Qlab not found; opening port ' + ports_out[1]
    midi_out.open_port(1)

#click logic
if click_iteration == 0:
    print 'sending 00'
    midi_out.send_message([0x90,0,0]) #ch, note, vel
if click_iteration == 1:
    print 'sending 01'
    midi_out.send_message([0x90,0,1]) #ch, note, vel
if click_iteration == 2:
    print 'sending 02'
    midi_out.send_message([0x90,0,2]) #ch, note, vel
