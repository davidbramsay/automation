import array
from ola.ClientWrapper import ClientWrapper

def DmxSent(state):
  wrapper.Stop()

universe = 1

data = array.array('B')

data.append(255) #CH 1, brightness
data.append(50) #CH 2, red
data.append(50) #CH 3, green
data.append(255) #CH 4, blue
data.append(0) #CH 5, strobe rate
data.append(0) #CH 6, control mode
data.append(0) #CH 7, control mode val

for i in range(512-7): data.append(0)

wrapper = ClientWrapper()
client = wrapper.Client()
client.SendDmx(universe, data, DmxSent)
wrapper.Run()
