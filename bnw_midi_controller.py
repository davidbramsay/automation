import rtmidi
import time
import helpers
#MIDI server that:


#inside here, it will take midi from Qlab and trigger various things:
# CHANNEL => 1 means control lights individually
#         => 2 means control lights as a group
#         => 3 means control outlets individually
#         => 4 means control outlets as a group

# 2, dmxch, 0 = dmx ch set to bright white
# 2, dmxch, 1 = dmx ch set to bright red
# 2, dmxch, 2 = dmx ch set to dim red
# 2, dmxch, 3 = dmx ch set to dim white
# 2, dmxch, 4 = dmx ch set to dim blue
# 2, dmxch, 5 = dmx ch set to fade in brightness
# 2, dmxch, 6 = dmx ch set to fade out brightness
# 2, dmxch, 7 = dmx ch brightness off
# 3, 0, 0 = turn off all lights
# 3, 0, 1 = turn on all lights
# 3, 0, 2 = fade off all lights
# 3, 0, 3 = fade on all lights
# 4, outletnum, 0 = outlet off
# 4, outletnum, 1 = outlet on
# 4, outletnum, 2 = outlet toggle
# 5, 0, 0 = all outlets off
# 5, 0, 1 = all outlets on



#on cue 3, sending same command should toggle outlets and end anything playing
# should also send a different midi cue to fade back up lights in intro

#always send outlet cues before fade cues because fades will block

#Note OFF = 8, Note ON = 9

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()
        self.oc = helpers.OutletNetworkController()
        self.dmx = helpers.UKingController(4)

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime

        command = (message[0] >> 4)
        channel = message[0] & 0b00001111
        channel = channel + 1
        notenum = message[1]
        velocity = message[2]

        print("@%0.6f %r" % (self._wallclock, [command, channel, notenum, velocity]))

        if channel==2: #individual DMX
            dmxch = notenum
            if velocity==0:
                self.dmx.update_channel(dmxch, [255,255,255,255])
            if velocity==1:
                self.dmx.update_channel(dmxch, [255,255,0,0])
            if velocity==2:
                self.dmx.update_channel(dmxch, [10,255,0,0])
            if velocity==3:
                self.dmx.update_channel(dmxch, [10,255,255,255])
            if velocity==4:
                self.dmx.update_channel(dmxch, [10,0,0,255])
            if velocity==5:
                self.dmx.fade_in(dmxch)
            if velocity==6:
                self.dmx.fade_out(dmxch)
            if velocity==7:
                self.dmx.update_channel(dmxch, [0])

        if channel==3: #all DMX
            if velocity==0:
                self.dmx.update_channel(values=[0])
            if velocity==1:
                self.dmx.update_channel(dmxch, [255])
            if velocity==2:
                self.dmx.fade_in()
            if velocity==3:
                self.dmx.fade_out()

        if channel==4: #individual outlet
            if velocity==0:
                self.oc.set_outlet_state(notenum, False)
            if velocity==1:
                self.oc.set_outlet_state(notenum, True)
            if velocity==2:
                self.oc.toggle_outlet(notenum)

        if channel==5: #all outlets
            if velocity==0:
                self.oc.set_outlet_state(state=False)
            if velocity==1:
                self.oc.set_outlet_state(state=True)
            if velocity==2:
                self.oc.toggle_outlet()



print 'Getting Output Port...'
midi_out = rtmidi.MidiOut()
ports_out = midi_out.get_ports()
print ports_out

if 'QLab' in ports_out:
    print 'using QLab for output'
    midi_out.open_port(ports_out.index('QLab'))
else:
    print 'Qlab not found; opening port ' + ports_out[1]
    midi_out.open_port(1)

print 'Getting Input Port...'
midi_in = rtmidi.MidiIn()
ports_in = midi_in.get_ports()
print ports_in
print 'opening port ' + ports_in[0]
midi_in.open_port(0)

midi_in.set_callback(MidiInputHandler(0))

try:
    while True:
        time.sleep(.5)
except KeyboardInterrupt:
    print('')

finally:
    print("Exit.")
    midi_in.close_port()
    del midi_in
