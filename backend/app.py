import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading
from subprocess import check_output
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository
from selenium import webdriver
import smbus
from datetime import datetime, date
from ClassSPI import MCPclass
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from mfrc522 import SimpleMFRC522
import os


sensor_file_name = '/sys/bus/w1/devices/28-0183a800007d/w1_slave'
relais=24
buzzer=21
start=23
stop=18
ipfull=check_output(['hostname','--all-ip-addresses'])
ip=str(ipfull.decode(encoding='utf-8'))[:14]


forbidden_list=[]
dataTimer=0
temperatuur=0
alcohol=0
lock=0
startAlc=False
uitTimeS=0
uitTimeW=0
#LCD

I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LCD_BACKLIGHT  = 0x08  # On 0X08 / Off 0x00

ENABLE = 0b00000100 # Enable bit

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1) # Rev 2 Pi uses 1



def lcd_init():
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
def show_ip():
    global ip
    lcd_string("",LCD_LINE_1)
    lcd_string("",LCD_LINE_2)
    time.sleep(0.3)
    lcd_string("WIFI:",LCD_LINE_1)
    lcd_string(ip,LCD_LINE_2)

# Callbacks
def callbackALC(String):
    global startAlc
    startAlc = not startAlc
    print(startAlc)
    

# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


# Code voor Hardware
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relais, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(start,GPIO.RISING,callbackALC, bouncetime=600)
    GPIO.add_event_detect(stop,GPIO.RISING,Shutdown, bouncetime=600)
   

def onewire():
    while True:
        global sensor_file
        sensor_file = open(sensor_file_name,'r')
        line = sensor_file.readlines()[-1]
        uitkomst = line[line.rfind("t"):]
        geheel = uitkomst[2:]
        sensor_file.close
        testuren=geheel[:2] + ',' + geheel[3:]
        data=geheel[:2] + '.' + geheel[3:]
        # print(f'onewire {testuren}')
        global temperatuur
        temperatuur=data
        # print(f"temperatuur:{data}")
        time.sleep(1)
def MeetAlcData():
    while True:
        klasse=MCPclass()
        global alcohol
        data=klasse.read_channel(1)
        alcohol=round((data/1023)*100,2) 
        print(f"alcohol:{alcohol}")
        klasse.closespi()
        time.sleep(1)

def dataTemp():
    while True:
        global temperatuur
        global dataTimer
        if dataTimer==60:
            print("Thread")
            DeviceID=2
            ActieID=3
            Datum=datetime.now()
            Waarde=float(temperatuur)
            Commentaar='Temperatuursmeting'
            DataRepository.create_log(DeviceID,ActieID,Datum,Waarde,Commentaar)
            # return testuren
            print(Waarde)
            socketio.emit('TempData', {'temperatuur': f'{Waarde}'})
            dataTimer=0
        dataTimer+=1
        time.sleep(1)

def loop_main():
    global startAlc
    global uitTimeS
    global uitTimeW
    while True:
        # print('loop')
        if startAlc is True:
            MeetAlcohol()
        if uitTimeS>0:
            uitTimeS=uitTimeS-1
            print(f's:{uitTimeS}')
            socketio.emit('Sluiting',{'time': uitTimeS,'id':933210265772})
            time.sleep(1)

        if uitTimeW>0:
            uitTimeW=uitTimeW-1
            print(f'w:{uitTimeW}')
            socketio.emit('Sluiting',{'time': uitTimeW,'id':453047185099})
            time.sleep(1)


        if uitTimeS<=0 :
            socketio.emit('Sluiting',{'time': uitTimeS,'id':933210265772})
            contactor('0','933210265772')
            time.sleep(1)

            
        if uitTimeW<=0:
            socketio.emit('Sluiting',{'time': uitTimeW,'id':453047185099})
            contactor('0','453047185099')
            time.sleep(1)

def MeetAlcohol():
    global startAlc
    global uitTimeW
    global uitTimeS
    lcd_string("",LCD_LINE_1)
    lcd_string("",LCD_LINE_2)
    time.sleep(1)
    lcd_string("Scan Badge",LCD_LINE_1)
    lcd_string("",LCD_LINE_2)
    time.sleep(3)
    id=rfid()
    # naam='shankar'
    list_forbidden=DataRepository.read_toegang(id)
    dict_forbidden=list_forbidden[0]
    toegang=dict_forbidden['Toegang']
    print(toegang,id)
    control=0
    if(id==933210265772):
        control=uitTimeS
    else:
        control=uitTimeW

    if control > 0:
        lcd_string("",LCD_LINE_1)
        lcd_string("",LCD_LINE_2)
        time.sleep(1)
        lcd_string("Kan niet scannen.",LCD_LINE_1)
        lcd_string("Timeout",LCD_LINE_2)
        time.sleep(2)
        startAlc = not startAlc
        show_ip()
    else:
        lcd_string("",LCD_LINE_1)
        lcd_string("",LCD_LINE_2)
        time.sleep(1)
        lcd_string("Scan OK",LCD_LINE_1)
        time.sleep(3)
        lcd_string("",LCD_LINE_1)
        lcd_string("",LCD_LINE_2)
        time.sleep(1)
        lcd_string("Blaas 5 seconden",LCD_LINE_1)
        lcd_string("In de sensor",LCD_LINE_2)
        setup_gpio()
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.5)
        hoogstalcohol=0
        lcd_string("",LCD_LINE_1)
        lcd_string("",LCD_LINE_2)
        lcd_string("Blijven blazen!",LCD_LINE_1)
        GPIO.output(buzzer,GPIO.HIGH)
        for i in range(0,6):
            global alcohol
            if alcohol>hoogstalcohol:
                hoogstalcohol=alcohol
            lcd_string(f"{i} s ; {hoogstalcohol}%",LCD_LINE_2)
            time.sleep(1)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.5)
        lcd_string("",LCD_LINE_1)
        lcd_string("",LCD_LINE_2)
        lcd_string(f"Resultaat: {hoogstalcohol}%",LCD_LINE_1)
        time.sleep(2)
        DeviceID=1
        ActieID=3
        Datum=datetime.now()
        Waarde=float(hoogstalcohol)
        Commentaar='Alcoholmeting'
        DataRepository.create_log(DeviceID,ActieID,Datum,Waarde,Commentaar)
        list_userID=DataRepository.read_userID(id)
        # print(dict_userID)
        dict_userID=list_userID[0]
        UserID=dict_userID['UserID']
        ADatum=Datum
        AWaarde=Waarde
        DataRepository.create_alc_log(UserID,ADatum,AWaarde)
        socketio.emit('AlcoholData', {'alcohol': f'{hoogstalcohol}'})
        print(f"Resultaat: {hoogstalcohol}")
        startAlc = not startAlc
        check_alcohol(hoogstalcohol,id)
def check_alcohol(percentage,id):
    if percentage >=48.88:      # 400 (limit)/1023*100
        DataRepository.update_toegang('0',id)
        contactor('3',id)
    elif percentage>=70.00:
        DataRepository.update_toegang('0',id)
        contactor('6',id)
    else:
        DataRepository.update_toegang('1',id)
        contactor('0',id)

def contactor(tijd,id):
    global uitTimeS 
    global uitTimeW
    # setup_gpio()
    list_forbidden=DataRepository.read_toegang(id)
    dict_forbidden=list_forbidden[0]
    toegang=dict_forbidden['Toegang']
    if str(tijd) == '3':
        if int(id)==933210265772:
            uitTimeS=40
        elif int(id)==453047185099:
            uitTimeW=40
        GPIO.output(relais,GPIO.LOW)
        lcd_string("Geblokkeerd",LCD_LINE_1)
        lcd_string("Voor 3 uur",LCD_LINE_2)
        time.sleep(2)
        show_ip()
    elif str(tijd) == '6':
        if int(id)==933210265772:
            uitTimeS=360
        elif int(id)==453047185099:
            uitTimeW=360

        GPIO.output(relais,GPIO.LOW)
        lcd_string("U mag niet rijden",LCD_LINE_1)
        lcd_string("Voor 6 uur",LCD_LINE_2)
        time.sleep(1)
        show_ip()
    elif str(tijd) == '0' and toegang==1:
        GPIO.output(relais,GPIO.HIGH)
        time.sleep(5)
        GPIO.output(relais,GPIO.LOW)
        DataRepository.update_toegang('0',id)
     

def rfid():
    global reader
    reader = SimpleMFRC522()
    reader.__init__()
    id, text = reader.read()
    print(id)
    print(text)
    reader.close_spi()
    return id

def Shutdown(String):
    # lcd_string("Shut Down",LCD_LINE_1)
    # lcd_string("Farewell!",LCD_LINE_2)
    # time.sleep(2)
    # os.system("sudo shutdown -h now")
    pass



# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/api/v1/history/', methods=['GET'])
def read_history():
    print('Get History')
    result = DataRepository.read_history()
    return jsonify(result)

@app.route('/api/v1/users/', methods=['GET'])
def read_users():
    print('Get users')
    result = DataRepository.read_users()
    return jsonify(result)
@app.route('/api/v1/alchistory/', methods=['GET'])
def read_alc_historiek():
    print('Get users')
    result = DataRepository.read_alc_history()
    return jsonify(result)

#SocketIO
@socketio.on('connect')
def initial_connection():
    print('A new client connected')


@socketio.on('F2B_locktime')
def LockTime(time,id):
    if time=='3':
        print(f'tijd {time} id={id}')
        check_alcohol(3,id)
    elif time=='6':
        print(f'tijd {time} id={id}')
        check_alcohol(6,id)
    elif time=='0':
        print(f'tijd {time} id={id}')
        check_alcohol(0,id)
#ChromeThread
def start_chrome_kiosk():
    import os

    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')         
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")
    while True:
        pass


def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()

def start_temp_thread():
    print("**** Starting TEMP ****")
    Thread = threading.Thread(target=onewire, args=(), daemon=True)
    Thread.start()

def start_tempData_thread():
    print("**** Starting TEMPData ****")
    ThreadData = threading.Thread(target=dataTemp, args=(), daemon=True)
    ThreadData.start()
def start_alcohol_thread():
    print("**** Starting ALC ****")
    ThreadAlc = threading.Thread(target=MeetAlcData, args=(), daemon=True)
    ThreadAlc.start()
def thread():
    print("**** Starting Loop ****")
    Threads = threading.Thread(target=loop_main, args=(), daemon=True)
    Threads.start()

# ANDERE FUNCTIES


if __name__ == '__main__':
    setup_gpio()
    lcd_init()
    GPIO.output(relais,GPIO.LOW)
    try:
        lcd_string("Welkom Bij",LCD_LINE_1)
        lcd_string("Alco-CarLock",LCD_LINE_2)
        time.sleep(3)
        show_ip()
        # setup_gpio()
        start_chrome_thread()
        start_temp_thread()
        start_tempData_thread()
        start_alcohol_thread()
        thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0',port=5000)
                
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()

