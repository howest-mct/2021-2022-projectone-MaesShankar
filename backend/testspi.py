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

        data=read_spi(1)
        alcohol=round((data/1024)*3.3,2) 
        RS_gas = ((5.0 * 2000)/alcohol) - 2000
        R0 = 16000
        ratio = RS_gas/R0 # ratio = RS/R0
        x = 0.4*ratio   
        global BAC
        BAC = pow(x,-1.431)/20  #BAC in mg/L
        print(f"alcohol:{round(BAC,2)}")
        time.sleep(1)

    
 
except KeyboardInterrupt:
  spi.close()