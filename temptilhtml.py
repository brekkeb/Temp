#!/usr/bin/python
import HTML
import os, glob, time, gspread, sys, datetime, random

#Google Auth
email = '*' #Set your email here
password = '*' #Set your password here
spreadsheet = '*' #Set the name of your spreadsheet here

#Try connecting to Google
try:
    gc = gspread.login(email,password)
except:
    print 'Failed to login...'
    sys.exit()

#Readies the spreadsheet
worksheet = gc.open(spreadsheet).sheet1

#Start temp.sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Set placement of sensor in system
device_folder = glob.glob('/sys/bus/w1/devices/"?"')
device_folder = [device_folder[0] + '/w1_slave', device_folder[1] + '/w1_slave']

#Read raw data
def read_temp_raw():
    f_1 = open(device_file[0], 'r')
    lines_1 = f_1.readlines()
    f_1.close()
    f_2 = open(device_file[1], 'r')
    lines_2 = f_2.readlines()
    f_2.close()

#Check connection and information
def read_temp():
    lines = read_temp_raw()
    while lines