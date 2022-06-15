import spidev
import time
spi = spidev.SpiDev()
class MCPclass:
    def __init__(self,bus=0,device=1):
        global spi
        spi.open(bus,device)
        spi.max_speed_hz = 10 ** 5

    def read_channel(self,ch):
        spidata = spi.xfer2([1,(8|ch)<<4,0])
        return ((spidata[1] & 3) << 8) + spidata[2]

    def closespi(self):
        global spi
        spi.close()

while True:
    klasse=MCPclass()
    data=klasse.read_channel(1)
    alcohol=round((data/1024)*3.3,2) 
    RS_gas = ((5.0 * 2000)/alcohol) - 2000
    R0 = 16000
    ratio = RS_gas/R0 # ratio = RS/R0
    x = 0.4*ratio   
    BAC = pow(x,-1.431)/20  #BAC in mg/L
    print(f"alcohol:{round(BAC,2)}")
    klasse.closespi()
    time.sleep(1)