#!/Users/davidramsay/.virtualenvs/audio-wrapper/bin/python

#must have flic_state_server.py running in the background
PORT = 12345
import rpyc

#connect and get current click and any other state we want to store
conn = rpyc.connect("localhost", PORT)
state_server = conn.root
click_num = state_server.i()

#check we got it
#print 'click #' + str(click_num)

#click logic
if click_num == 0:
    pass
    #print 'things we want to happen on the first click'

if click_num == 1:
    pass
    #print 'things we want to happen on the second click'

if click_num == 2:
    pass
    #print 'things we want to happen on the third click'
