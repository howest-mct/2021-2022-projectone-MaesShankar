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
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
sensor_file_name = '/sys/bus/w1/devices/28-0183a800007d/w1_slave'

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


# Code voor Hardware
def setup_gpio():
    pass

def onewire():
    global sensor_file
    sensor_file = open(sensor_file_name,'r')
    line = sensor_file.readlines()[-1]
    uitkomst = line[line.rfind("t"):]
    geheel = uitkomst[2:]
    sensor_file.close
    testuren=geheel[:2] + ',' + geheel[3:]
    data=geheel[:2] + '.' + geheel[3:]
    # print(f'onewire {testuren}')
    time.sleep(1)
    DeviceID=2
    ActieID=3
    Datum=datetime.now()
    Waarde=float(data)
    Commentaar='Temperatuursmeting'
    DataRepository.create_log(DeviceID,ActieID,Datum,Waarde,Commentaar)
    return testuren

# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)



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

#SocketIO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    waarde=onewire()
    emit('B2F_connected', {'temperatuur': f'{waarde}'})

@socketio.on('AskTemp')
def Temperatuur():
    temperatuur=onewire()
    emit('TempData', {'temperatuur': f'{temperatuur}'})

@socketio.on('F2B_locktime')
def LockTime(time):
    print(f'tijd {time}')

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



# ANDERE FUNCTIES


if __name__ == '__main__':
    setup_gpio()
    lcd_init()

    try:
        lcd_string("Welkom Bij",LCD_LINE_1)
        lcd_string("Alco-CarLock",LCD_LINE_2)
        time.sleep(3)
        lcd_string("",LCD_LINE_1)
        lcd_string("",LCD_LINE_2)
        ipfull=check_output(['hostname','--all-ip-addresses'])
        ip=str(ipfull.decode(encoding='utf-8'))[:15]
        lcd_string("WIFI:",LCD_LINE_1)
        lcd_string(ip,LCD_LINE_2)
        # setup_gpio()
        start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0',port=5000)
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()

