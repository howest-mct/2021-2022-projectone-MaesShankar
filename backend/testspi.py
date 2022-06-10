import spidev
import time
from RPi import GPIO

GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 10 ** 5  

def read_spi(channel):
  spidata = spi.xfer2([1,(8+channel)<<4,0])
  return ((spidata[1] & 3) << 8) + spidata[2]

try:
  while True:
    channeldata = read_spi(1)
    channeldata=(channeldata/1023)*100
    print("Waarde POT = {}".format(round(channeldata,2)))
    time.sleep(2)
    
 
except KeyboardInterrupt:
  spi.close()