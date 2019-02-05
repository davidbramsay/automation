import pytuya

d = pytuya.OutletDevice('20156003840d8e48246a', '192.168.1.130', '8c728099a26db945')

#get and print status
data = d.status()  # NOTE this does NOT require a valid key
print('Dictionary %r' % data)
print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device

# Toggle switch state
switch_state = data['dps']['1']
data = d.set_status(not switch_state)  # This requires a valid key
