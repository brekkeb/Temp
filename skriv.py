#!/usr/bin/env python

#Imports important modules
from multiprocessing import Process, Queue
import time, subprocess, os, thread, threading

os.system('cls' if os.name == 'nt' else 'clear')

print 'Options found'
print 'Loading options'
time.sleep(1)

#Threads
def tMeny(q):
    time.sleep(1)
    options()
def tRun(q):
    execfile('temp.py')
q = Queue()
tMeny = Process(target=tMeny, args=(q,))
tRun = Process(target=tRun, args=(q,))

#Options
def options():
    def menu():
        print '1# Start temp.sensor script'
        print '2# Stop temp.sensor script'
        print '3# Start logging locally'
        print '4# Print previous results'
        print '5# Exit'
        print '6# Print status of threads'

    menu()
    foo = raw_input('Option #:')
    if foo == '1':
        print 'Starting temp.sensor script now'
        tMeny.start()
        tRun.start()
        print
        #Just checking status of threads at runtime, both should be True
        print 'tMeny thread is active: ', tMeny.is_alive()
        print
        print 'tRun thread is active:  ', tRun.is_alive()
        print
        options()
    elif foo == '2':
        #Stopping temp.sensor script
        print 'Stopping temp.sensor script now'
        tMeny.terminate()
        tRun.terminate()
        print
        options()
    elif foo == '3':
        #Logging results locally, doesn't do anything as of now
        print 'Logging results locally'
        print
        options()
    elif foo == '4':
        #Printing prev results, doesn't do anything as of now
        print 'Finding previous results'
        print
        options()
    elif foo == '5':
        #Exiting everything
        print 'Exiting...'
        if tMeny.is_alive() == True:
            tMeny.terminate()
        if tRun.is_alive() == True:
            tRun.terminate()
        exit()
    elif foo == '6':
        #Checks which threads is active
        print 'Status of threads:'
        print
        print 'tMeny is active: ', tMeny.is_alive()
        print
        print 'tRun is active:  ', tRun.is_alive()
        print
        options()
    else:
        #If none parameters fit, do this
        print 'Failure to understand'
        print
        options()
options()
