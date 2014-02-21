#!/usr/bin/env python

import os, glob, time, gspread, sys, datetime, random

#Google auth
email = 'disclosed'
password = 'disclosed'
spreadsheet = 'Temp_LOG' #Navnet til regnearket på Google

#Prøv å koble til Google
try:
    gc = gspread.login(email,password)
except:
    print 'Failed to login...'
    sys.exit()

#Klargjør regnearket
worksheet = gc.open(spreadsheet),sheet1

#Start temp.sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Sett plassering til sensor i systemet
device_folder = glob.glob('/sys/bus/w1/devices/"?"') #Erstatt med enhetsID
device_folder = [device_folder[0] + '/w1_slave', device_folder[1] + '/w1_slave']

#Funksjon for å lese rå data fra sensor
def read_temp_raw():
    f_1 = open(device_file[0], 'r')
    lines_1 = f_1.readlines()
    f_1.close()
    f_2 = open(device_file[1], 'r')
    lines_2 = f_2.readlines()
    f_2.close()
    return lines_1 + lines_2

#Sjekker tilkobling og trekker ut informasjon fra sensor
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t='), lines[3].find('t=')
    temp = float(lines[1][equals_pos[0]+2:])/1000, float(lines[3][equals_pos[1]+2:])/1000
    return temp

#Uendelig loop om noe er sant
while True:
    temp = read_temp()
    values = [datetime.datetime.now(), values]
    worksheet.append_row(values)
    time.sleep(10)
