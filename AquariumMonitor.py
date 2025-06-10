from flask import Flask, render_template, request, make_response, jsonify, send_from_directory
from datetime import datetime
# Use the below import if using an authentication system
#from AuthUtils import auth_required
from gpio_client import register, set_gpio, get_gpio
import pytz
import time
import os

# import custom module created
import DS18b20_Module
import DBUtilities as dbutils
import JSONUtilities as js


app=Flask(__name__)

# Initialise the DS18B20 temperature sensor
temperatureSensor = DS18b20_Module.DS18b20()

@app.route('/')
#@auth_required
def index():

    [co2start,co2stop] = js.getStartAndStopTime('co2')
    [rgbstart,rgbstop] =js.getStartAndStopTime('rgb')
    [whitestart,whitestop] = js.getStartAndStopTime('white')
    curTime = datetime.now()
    curTimeStr = curTime.strftime("%H:%M")
    curTimeStampStr = curTime.strftime("%D  %H:%M")
    curDate = curTime.strftime("%D")
    
    co2manualOverride = js.getManualOverride('co2')
    whitemanualOverride = js.getManualOverride('white')
    rgbmanualOverride = js.getManualOverride('rgb')

    co2PinState = get_gpio("co2").get("state")
    whiteLightState = get_gpio("white").get("state")
    rgbLightState = get_gpio("rgb").get("state")
    
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
        curTemp,minTemp, minTempTime, maxTemp, maxTempTime =dbutils.getMaxMinAndCurrentTempData(curDate)
    except:
        curTemp="NaN"
        minTemp="NaN"
        minTempTime="NaN"
        maxTemp="NaN"
        maxTempTime="NaN"

    devices = {
        'co2': {
            'start': co2start,
            'stop': co2stop,
            'state': co2PinState,
            'checked': co2checkboxVal
        },
        'rgb': {
            'start': rgbstart,
            'stop': rgbstop,
            'state': rgbLightState,
            'checked': rgbcheckboxVal
        },
        'white': {
            'start': whitestart,
            'stop': whitestop,
            'state': whiteLightState,
            'checked': whitecheckboxVal
        }
    }
    
    data = {
        'title': 'My Aquarium Page',
        'timestamp': curTimeStampStr,
        'time':curTimeStr,
        'gantturl': gantChartURL,
        'minTemp': minTemp,
        'minTempTime': minTempTime,
        'maxTemp': maxTemp,
        'maxTempTime': maxTempTime,
        'currentTemp': curTemp,
        'devices': devices  # << ✅ add this
    }
    return render_template('index.html', **data)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<deviceName>/<action>', methods=['POST'])
#@auth_required
def action(deviceName, action):
    curTime = datetime.now().time()
    [startTime_str,stopTime_str] = js.getStartAndStopTime(deviceName)
    startTime = datetime.strptime(startTime_str,"%H:%M").time()
    stopTime = datetime.strptime(stopTime_str,"%H:%M").time()

    status = 'unchanged';
    
    if(curTime < startTime or curTime > stopTime):
        if action =="toggle":
            manual = js.getManualOverride(deviceName)
            if manual:
                js.updateManualOverride(deviceName, False)
                set_gpio(deviceName, False)
                status = 'off'
            else:
                js.updateManualOverride(deviceName, True)
                set_gpio(deviceName, True)
                status = 'on'

    return jsonify({'status': status})

@app.route('/timer', methods=["GET","POST"])
#@auth_required
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
    embed = request.args.get('embed') == 'true'
    return render_template("temperature_chart.html")

@app.route('/temperature_chart_data')
def temperature_chart_data():
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

    chart_data = dbutils.getDataForChart(start_date, end_date)
    return jsonify(chart_data)

if __name__=='__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
    #app.run(host='0.0.0.0')

