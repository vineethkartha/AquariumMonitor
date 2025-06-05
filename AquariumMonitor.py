from flask import Flask, render_template, request, make_response, jsonify
from AuthUtils import auth_required
import DS18b20_Module
import DBUtilities as dbutils
import JSONUtilities as js
#import picamera
import time
import RPi.GPIO as GPIO
from datetime import datetime
import pytz
import sqlite3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
whiteLight = 6
rgbLight = 5
co2system = 26

GPIO.setup(whiteLight, GPIO.OUT)
GPIO.setup(rgbLight, GPIO.OUT)
GPIO.setup(co2system, GPIO.OUT)

app=Flask(__name__)

# Uncomment this if you have a temperature sensor 
temperatureSensor = DS18b20_Module.DS18b20()

@app.route('/')
@auth_required
def index():
    ## Uncomment the below camera section if you plan to use a picamera
    #camera = picamera.PiCamera()
    #time.sleep(.5)
    #camera.resolution = (800, 600)
    #camera.vflip = True
    #camera.capture('/home/vineeth/AquariumMonitor/static/images/aquarium.jpg')
    #camera.close()

    [co2start,co2stop] = js.getStartAndStopTime('co2')
    [rgbstart,rgbstop] =js.getStartAndStopTime('rgb')
    [whitestart,whitestop] = js.getStartAndStopTime('white')
    curTime = datetime.now()
    curTimeStr = curTime.strftime("%D  %H:%M")
    curDate = curTime.strftime("%D")
    
    co2manualOverride = js.getManualOverride('co2')
    whitemanualOverride = js.getManualOverride('white')
    rgbmanualOverride = js.getManualOverride('rgb')

    co2PinState = GPIO.input(co2system)
    whiteLightState = GPIO.input(whiteLight)
    rgbLightState = GPIO.input(rgbLight)
    
    if co2manualOverride:
        co2checkboxVal = "checked"
    else:
        co2checkboxVal = ""
        
    if whitemanualOverride:
        whitecheckboxVal = "checked"
    else:
        whitecheckboxVal = ""

    if rgbmanualOverride:
        rgbcheckboxVal = "checked"
    else:
        rgbcheckboxVal = ""

    gantChartURL = js.getGanttChartURL()
    try:
        curTemp,minTemp, minTempTime, maxTemp, maxTempTime,url =dbutils.getData(curDate)
    except:
        curTemp="NaN"
        minTemp="NaN"
        minTempTime="NaN"
        maxTemp="NaN"
        maxTempTime="NaN"
        url = "/static/images/error.png"
    data = {
        'title': 'My Aquarium Page',
        'time': curTimeStr,
        'url': url,
        'gantturl': gantChartURL,
        'minTemp': minTemp,
        'minTempTime': minTempTime,
        'maxTemp': maxTemp,
        'maxTempTime': maxTempTime,
        'currentTemp': curTemp,
        'co2start':co2start,
        'co2stop':co2stop,
        'rgbstart':rgbstart,
        'rgbstop':rgbstop,
        'whitestart':whitestart,
        'whitestop':whitestop,
        #'snapshot':'/static/images/aquarium.jpg?'+str(time.time()), #uncomment this if using a camera
        'whitecheckboxVal':whitecheckboxVal,
        'rgbcheckboxVal':rgbcheckboxVal,
        'co2checkboxVal':co2checkboxVal,
        'co2PinState':co2PinState,
        'whiteLightState':whiteLightState,
        'rgbLightState':rgbLightState        
        }
    print("Co2 state: ")
    print(curTemp)
    return render_template('index.html', **data)

@app.route('/<deviceName>/<action>', methods=['POST'])
@auth_required
def action(deviceName, action):
    curTime = datetime.now().time()
    [startTime_str,stopTime_str] = js.getStartAndStopTime(deviceName)
    startTime = datetime.strptime(startTime_str,"%H:%M").time()
    stopTime = datetime.strptime(stopTime_str,"%H:%M").time()
    if deviceName == 'white':
        device = whiteLight
    elif deviceName == 'rgb':
        device = rgbLight
    elif deviceName == 'co2':
        device = co2system
    else:
        return jsonify({'error: unknown device'}),400

    status = 'unchanged';
    
    if(curTime < startTime or curTime > stopTime):
        if action =="toggle":
            manual = js.getManualOverride(deviceName)
            if manual:
                js.updateManualOverride(deviceName, False)
                GPIO.output(device, GPIO.LOW)
                status = 'off'
            else:
                js.updateManualOverride(deviceName, True)
                GPIO.output(device, GPIO.HIGH)
                status = 'on'

    return jsonify({'status': status})

@app.route('/timer', methods=["GET","POST"])
@auth_required
def timersystem():
    if request.method == "POST":
        startTime = request.form.get("co2_start")
        stopTime = request.form.get("co2_stop")
        js.updateTimers('co2', startTime, stopTime)

        startTime = request.form.get("rgb_start")
        stopTime = request.form.get("rgb_stop")
        js.updateTimers('rgb', startTime, stopTime)

        startTime = request.form.get("white_start")
        stopTime = request.form.get("white_stop")
        js.updateTimers('white', startTime, stopTime)

        return render_template("timerset.html")


@app.route('/temperature_chart')
def temperature_chart():
    return render_template("temperature_chart.html")

@app.route('/temperature_chart_data')
def temperature_chart_data():
    dbName = '/home/vineeth/AquariumMonitor/data/temperatureLog.db'
    ist = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist).date()

    # Get query parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else today
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else start_date
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Date, Time, Temperature FROM AquariumTemperature
        WHERE Date BETWEEN ? AND ?
        ORDER BY Date ASC, Time ASC
    """, (start_date.strftime('%D'), end_date.strftime('%D')))
    rows = cursor.fetchall()
    conn.close()

    print(start_date.strftime('%D'))
    chart_data = [
        {
            'timestamp': f"{date} {time}",
            'temperature': round(temp, 1)
        } for date, time, temp in rows
    ]

    return jsonify(chart_data)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')

