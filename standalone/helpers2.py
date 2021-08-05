from ola.ClientWrapper import ClientWrapper
from scapy.all import arping
import numpy as np
import pytuya
import config
import time
import atexit
import array
import threading
from requests.exceptions import ConnectionError


def threaded_outlet_call(outlets, outlet, state):
    print('calling outlet thread')
    #outlet=None means we set state for all outlets
    if outlet is not None:
        successful = False
        counter = 0
        while not successful and counter<10:
            print('TRY',counter)
            try:
                outlets[outlet].set_status(state)
                print('light success')
                successful = True
            except:
                time.sleep(0.5+counter*0.5)
                counter+=1
                print('connection reset: trying with counter')

    else:
        retries=range(len(outlets))
        counter = 0
        while len(retries) and counter<10:
            print('TRY',counter)
            new_retries = []
            for i in retries:
                try:
                    outlets[i].set_status(state)
                    print('success for',i)
                except:
                    new_retries.append(i)
                    print('connection reset for',i)

            retries = new_retries
            time.sleep(0.5+counter*0.5)
            counter+=1

            if not len(retries):
                #seemed successful, double check
                result = []
                for o in outlets:
                    successful = False
                    while not successful:
                        try:
                            result.append(o.status()['dps']['1'])
                            successful = True
                        except:
                            pass
                print(result)

                for i in range(len(result)):
                    if result[i] != state:
                        retries.append(i)
                print('new retries:',retries)



class OutletNetworkController:

    mac_to_ip = {}
    addresses = ''
    outlet_configs = []
    outlets = []

    def __init__(self, addresses="192.168.1.*"):

        print 'searching ' + addresses
        print 'should find/add devices now (indicated by [FOUND])...'
        # find all MAC address -> IP mappings
        self.addresses = addresses
        ans, unans = arping(addresses)

        # add them to a dict
        for r in ans:
            mac = r[1].hwsrc
            ip = r[1].psrc
            self.mac_to_ip[mac] = ip

        print '\n'

        # run through MAC addresses in config and see if we have an IP
        for oc in config.outlets:
            ip = self.networking__lookup_mac(oc[2])

            # if we do, add it to outlet_configs and add the device to outlets
            if ip is not None:
                self.outlet_configs.append((oc[0], oc[1], ip))
                self.outlets.append(pytuya.OutletDevice(oc[0], ip, oc[1]))

                print '[FOUND] found and added ' + str(oc[0]) + \
                      ', device #' + str(len(self.outlets)-1)
        print '\nDone searching.\n'


    def networking__get_full_ip_lookup_table(self):
        return self.mac_to_ip


    def networking__lookup_mac(self, mac):
        if mac in self.mac_to_ip:
            return self.mac_to_ip[mac]
        else:
            return None


    def test_outlets(self):
        #toggle outlets 1 by 1 for testing
        print 'setting all devices off...'
        self.set_outlet_state(state=False)
        time.sleep(1)
        for i, o in enumerate(self.outlets):
            print '\nToggling device #' + str(i) + '...'
            print 'off'
            self.set_outlet_state(outlet=i,state=False)
            time.sleep(1)
            print 'on'
            self.set_outlet_state(outlet=i,state=True)
            time.sleep(2)
            print 'off'
            self.set_outlet_state(outlet=i,state=False)
            time.sleep(1)


    def toggle_outlet(self, outlet=None):
        #outlet=None means we toggle for all outlets
        if outlet is not None:
            current_state = self.get_outlet_state(outlet)
            self.outlets[outlet].set_status(not current_state)
        else:
            for i in range(len(self.outlets)):
                current_state = self.get_outlet_state(i)
                self.outlets[i].set_status(not current_state)


    def get_outlet_state(self, outlet=None):
        #outlet=None means we get state for all outlets
        #state is bool (True/False) depending on outlet
        if outlet is not None:
            return self.outlets[outlet].status()['dps']['1']
        else:
            result = []
            for o in self.outlets:
                result.append(o.status()['dps']['1'])

            return result


    def set_outlet_state(self, outlet=None, state=True):
        #outlet=None means we set state for all outlets
        outlet_thread = threading.Thread(target=threaded_outlet_call, args=(self.outlets, outlet, state))
        outlet_thread.daemon = True
        outlet_thread.start()

    def get_outlet_status(self, outlet=None):
        #outlet=None means we get state for all outlets
        #'status' includes device name and some other key
        if outlet is not None:
            return self.outlets[outlet].status()
        else:
            result = []
            for o in self.outlets:
                result.append(o.status())
            return result



# CH1: brightness
# CH2,3,4: R,G,B
# CH5: Strobe, 0 is none. 8-255 increases speed with larger #s
# CH6: 0 is default, controlled by CH1-5.
#      50 sets color to be interpolated/controlled by CH7 value.
#      100 sets color fade through all colors, speed by CH7 value.
#      150 sets color pulse through all colors, speed by CH7 value.
#      200 sets color swipe through all colors, speed by CH7 value.
#      250 sets in sound control mode.
# CH7: control value for CH6 setting.

class GlobalDmxState(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.state = array.array('B', [0]*512)
        self.modified = False

    def get(self):
        with self.lock:
            local_state = self.state
            local_modified = self.modified
            self.modified = False
        return local_state, local_modified

    def set(self, array):
        with self.lock:
            self.state = array
            self.modified = True



class DmxControlThread(threading.Thread):
    def __init__(self, name, ola_universe, dmx_state, interface_fs=30):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = name
        self.ola_universe = ola_universe
        self.dmx_state = dmx_state
        self.tick_interval = 1000./interface_fs

    def DmxSent(self, state):
        if not state.Succeeded():
            print 'DMX ERROR, NOT SUCCEEDED.'
            self.wrapper.Stop()

    def send_DMX(self):
        self.wrapper.AddEvent(self.tick_interval, self.send_DMX)

        new_state, modified = self.dmx_state.get()
        if modified:
            self.wrapper.Client().SendDmx(self.ola_universe,
                                            new_state,
                                            self.DmxSent)

    def close(self):
        print 'thread close'
        self.wrapper.Stop()

    def run(self):
        print 'starting DMX control thread'
        atexit.register(self.close)
        self.wrapper = ClientWrapper()
        self.wrapper.AddEvent(self.tick_interval, self.send_DMX)
        self.wrapper.Run()



class UKingController:
    def __init__(self, num_channels=4, ola_universe=1):
        print 'initializing UKing DMX controller with ' + \
              str(num_channels) + ' channels in universe ' + \
              str(ola_universe) + '.'

        self.num_channels = num_channels
        self.ch_indices = [1]
        self.ch_indices.extend(np.multiply(8,range(1,num_channels)).tolist())

        print 'LIGHTS SHOULD BE SET TO CHANNELS ' + str(self.ch_indices)

        self.dmx_state = GlobalDmxState()
        self.local_dmx_state = self.dmx_state.get()[0]
        self.dmx_controller = DmxControlThread('t1',
                                                ola_universe,
                                                self.dmx_state)

        self.dmx_controller.start()


    def update_channel(self, channel=None, values=[0,0,0,0,0,0,0]):
        #channel=None will update all channels
        if channel is not None:
            to_update = self.ch_indices[channel]-1
            for i,v in enumerate(values):
                self.local_dmx_state[to_update + i] = v
        else:
            for i,v in enumerate(values):
                for ch in self.ch_indices:
                    to_update = ch-1
                    self.local_dmx_state[to_update + i] = v

        self.dmx_state.set(self.local_dmx_state)


    def fade_in(self, channel=None, rate=1):
        for i in range(255):
            self.update_channel(channel, values=[i])
            time.sleep(rate/30.)


    def fade_out(self, channel=None, rate=1):
        for i in range(255):
            self.update_channel(channel, values=[255-i])
            time.sleep(rate/30.)


    def test_dmx(self):
        print 'setting all devices off...'
        self.update_channel() # resets all to zero
        time.sleep(1)
        for i in range(self.num_channels):
            print '\nToggling channel #' + str(i) + ', DMX #'+ str(self.ch_indices[i]) + '...'
            print 'off'
            self.update_channel(i)
            time.sleep(1)
            print 'on'
            self.update_channel(i, [255,255,255,255]) #bright, RGB
            time.sleep(2)
            print 'off'
            self.update_channel(i)
            time.sleep(1)



if __name__=='__main__':
    outletctl = OutletNetworkController("192.168.2.*")
    outletctl.test_outlets()

    '''
    print outletctl.get_outlet_status()
    print outletctl.get_outlet_state()

    print outletctl.get_outlet_status(0)
    print outletctl.get_outlet_state(0)

    outletctl.toggle_outlet()
    outletctl.toggle_outlet(0)
    outletctl.toggle_outlet()

    outletctl.test_outlets()
    '''

    dmx = UKingController(4)
    dmx.test_dmx()
    dmx.update_channel(values=[0,255,255,255])
    dmx.fade_in()
    dmx.fade_out()

