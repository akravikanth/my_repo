#!/usr/bin/env python

import sys
import datetime

from jnpr.jet.notification.NotificationHandler import *
from jnpr.jet.notification.NotificationTopic import *
from jnpr.jet.route.RouteService import *
from jnpr.jet.shared.ttypes import *
from jnpr.jet.JetHandler import *
from whatsapp import Client
from pprint import pprint as pp

import ConfigParser
import getopt
import os
import sys
import twitter

# JET server details
DEVICE_IP = "10.216.xx.xx"
DEVICE_PORT = 9090
DEVICE_NOT_PORT = 1883

MY_IP = "10.216.xx.xx"

#Whatsapp credentials

w_client = Client(login = '91xxxxxxxxxx', password = 'OsYWl1OlwEx7kndguVsQ5t9zUfE=')
to_phone = '91XXXXXXXXXX'

"""
 Post update to Whatsapp 
"""

def postWhatsapp(sub, msg, host_name):
    try:
        wpost = sub + "\n" + msg
        wpost += "\n IP: " + MY_IP
        wpost += "\n Host: " + host_name
        wpost +=  "\n On: " + str(datetime.datetime.now())
        wpost += "\n@akravikanth"
        wpost = wpost.encode('utf-8')
        w_client.send_message(to_phone,wpost)
    except TypeError as e:
        print "Ignore the error"
	print e.message
        #sys.exit(2)


"""
Handle interface related events
"""
def interfaceEventHandler(sub, message):
    text = "Interface Name: " + message['jet-event']['attributes']['name']
    host_name = message['jet-event']['hostname'];
    #postTweet(sub, text, host_name)
    postWhatsapp(sub, text, host_name)
    return

"""
Handler to build message based on event received and take action
"""
def handleEvents(message):
    event_name = message['jet-event']['event-id']
    print "*****Notification message:type=", event_name, " *****"
    if (event_name == 'KERNEL_EVENT_IFD_CHANGE'):
	    interfaceEventHandler("Interface Changed", message)
    return


"""
Enter the JET
"""
try:
    # Create a client handler for connecting to server
    client = JetHandler()

    # Open connection to the server
    print "***Opening connection to device***"
    #client.OpenRequestResponseSession(device=DEVICE_IP, port=DEVICE_PORT)

    # Create an event handler for notification subscription
    client.OpenNotificationSession(device=DEVICE_IP, port=DEVICE_NOT_PORT,user=None, password=None, tls=None, bind_address="", is_stream = False)
    evHandle = client.GetNotificationService()


    ifdtopic = evHandle.CreateIFDTopic(op=evHandle.ALL)

    # Subscribe for events
    print "Subscribing to IFD notifications"
    evHandle.Subscribe(ifdtopic, handleEvents)


    # Wait for events
    while True:
	pass
    
    # Unsubscribe events
    print "***Unsubscribe from all the event notifications***"
    evHandle.Unsubscribe()

    print "***Closing the Client***"
    evHandle.close()
    client.CloseNotificationSession()
except Exception, tx:
    print '%s' % (tx.message)
