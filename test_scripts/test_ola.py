import array
from ola.ClientWrapper import ClientWrapper

wrapper = None
loop_count = 0
TICK_INTERVAL = 50  # in ms

def DmxSent(state):
  if not state.Succeeded():
    wrapper.Stop()

def SendDMXFrame():
  # schdule a function call in 100ms
  # we do this first in case the frame computation takes a long time.
  wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)

  # compute frame here
  data = array.array('B')
  global loop_count
  data.append(loop_count % 255)
  data.append(0)
  data.append(0)
  data.append(255)
  data.append(0)
  data.append(0)
  data.append(0)
  for i in range(512-7):
      data.append(0)

  loop_count += 1

  # send
  wrapper.Client().SendDmx(1, data, DmxSent)


wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()
