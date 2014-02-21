#!/usr/bin/python
# encoding: utf-8
import subprocess
import datetime
import time

#This is where the generated HTML file will be saved. Make sure the destination folder has the correct permissions
htmlFilePath = '/var/www/temp/index.html'

#The time in seconds before updating again
waitTime = 10

def detectSensors():
    sensorList = subprocess.check_output('ls -1 /sys/bus/w1/devices/', shell=True)
    sensorList = sensorList.splitlines()
    sensorList.remove('w1_bus_master1')
    sensorList.insert(0, 0)
    return sensorList

def pollSensor(sensorId):
    sensorFile = open('/sys/bus/w1/devices/' + sensorId + '/w1_slave')
    sensorLines = sensorFile.readlines()
    sensorFile.close()

    if sensorLines[0].strip()[-3:] == 'YES':
        equalsPosition1 = sensorLines[1].find('t=')
        sensorCelsius = float(sensorLines[1][equalsPosition1+2:])/1000
        return sensorCelsius

    else:
        print 'CRC Failed on Sensor: ' + sensorId
        return 'CRCFailed'

def generateHtml(tempArray):
    htmlOut = open(htmlFilePath, 'w')
    htmlOut.write('<head><title>Sensors @ RasPi Webtemp</title></head>')
    htmlOut.write('<body><h1>Raspberry Pi Temperature Sensors</h1>')
    htmlOut.write('<table border=1>')
    for i in range(1,len(sensorPath)):
        if tempArray[i] != 'CRCFailed':
            htmlOut.write('<tr><th>Sensor %s</th><td> %s *C</td></tr>' % (i, tempArray[1]))
        else:
            htmlOut.write('<tr><th>Sensor %s</th><td> CRC Failed</td></tr>' % i)
    htmlOut.write('</table>')
    htmlOut.write('<p>Page generated: %s</p>' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    htmlOut.write('</body>')
    htmlOut.close()

subprocess.call('modprobe w1-gpio', shell=True)
subprocess.call('modprobe w1-therm', shell=True)

#Comment out 'sensorPath = detectSensors()' and uncomment the line below to manually specify sensors
#sensorPath = [0, '28-000002dc0390', '28-000002dc0671']
sensorPath = detectSensors()

while True:
    sensorTemp = dict()
    for i in range(1, len(sensorPath)):
        sensorTemp[i] = pollSensor(sensorPath[i])
        print 'Sensor ' +str(i) + ': ' + str(sensorTemp[i])
        if sensorTemp[i] > 30 and sensorTemp[i] != 'CRCFailed':
            pushNotify('High Temperature Alert', 'Sensor ' + str(i) + ': ' + str(sensorTemp[i]))
            print 'Notification Sent'

    print 'Generating HTML'
    generateHtml(sensorTemp)
    print 'HTML Saved'
    time.sleep(waitTime)