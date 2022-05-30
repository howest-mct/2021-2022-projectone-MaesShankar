import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

from selenium import webdriver

sensor_file_name = '/sys/bus/w1/devices/28-0183a800007d/w1_slave'
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options




    

# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

# # Code voor Hardware
def setup_gpio():
    pass

def onewire():
    global sensor_file
    sensor_file = open(sensor_file_name,'r')
    line = sensor_file.readlines()[-1]
    uitkomst = line[line.rfind("t"):]
    geheel = uitkomst[2:]
    temperatuur = 'De temperatuur is ' + geheel[:2] + ',' + geheel[2:]+'°Celsius'
    sensor_file.close
    testuren=geheel[:2] + ',' + geheel[3:]
    print(f'onewire {testuren}')
    time.sleep(1)
    socketio.emit('TempData', {'temperatuur': f'{12}'},broadcast=True)

# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/api/v1/history/', methods=['GET'])
def read_history():
    print('Get History')
    result = DataRepository.read_history()
    return jsonify(result)

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    onewire()
    
    


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

def start_Temp_Thread():
    print("**** Starting TEMP ****")
    tempThread = threading.Thread(target=onewire, args=(), daemon=True)
    tempThread.start()


# ANDERE FUNCTIES


if __name__ == '__main__':
    try:
        # setup_gpio()
        print("**** Starting Thread ****")
        start_chrome_thread()
        # start_Temp_Thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0',port=5000)
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()

