import rtmidi
import time

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))


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
#midi_out.send_message([0x90,0,0]) #ch, note, vel

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')

finally:
    print("Exit.")
    midi_in.close_port()
    del midi_in
