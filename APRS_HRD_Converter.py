#!/usr/bin/env python

import socket
import time
import aprslib
import os
from configparser import ConfigParser

# Name of the config file
nameOfConfig = "config.ini"

# Config parser for settings
config = ConfigParser()

# Client which is used to connect
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# save the config
def save_config():
    with open(nameOfConfig, 'w') as f:
        config.write(f)
        
def init_of_config():
    if not(os.path.exists(nameOfConfig)):
        user = input ("Enter your Callsign: ")
        password = input ("Enter your password for APRS: ")
        desc = input ("Enter your description (example: John Doe from T08): ")
        pos_N = input ("Enter your position - N-Part (xxxx.xxN): ")
        pos_E = input ("Enter your position - E-Part (xxxxx.xxE): ")

        
        config.read(nameOfConfig)
        config.add_section('Main config')
        config.set('Main config', 'APRS_User', user)
        config.set('Main config', 'APRS_PW', password)
        config.set('Main config', 'APRS_Desc', desc)
        config.add_section('Position')
        config.set('Position', 'Pos_N', pos_N)
        config.set('Position', 'Pos_E', pos_E)
        save_config()
    
    config.read(nameOfConfig)

# connect to the HRD IP server
def connect_to_HRD():
    # HRD IP server is connectable at localhost and port 7809
    client.connect(('127.0.0.1', 7809))

# Construct a valid HRD IP server frame
def construct_frame(command):
    array_frame_signature = bytes([0xcd, 0xab, 0x34, 0x12, 0x34, 0x12, 0xcd, 0xab])
    array_frame_4_zerobytes = bytes([0x00, 0x00, 0x00, 0x00])
    array_frame_end = bytes([0x00, 0x00, 0x00, 0x00 , 0x00 , 0x00])

    array_frame_payload = bytes()
    
    encodedutf8 = command.encode("utf-8")
    for x in range(0, len(encodedutf8)):
        array_frame_payload += bytes([encodedutf8[x], 0x00])
        
    lengthOfFrame = 22 + (len(array_frame_payload))

    array_frame_length = bytes([lengthOfFrame & 0xff, (lengthOfFrame>>8) & 0xff, (lengthOfFrame>>16) & 0xff, (lengthOfFrame>>24) & 0xff])
    
    return array_frame_length + array_frame_signature + array_frame_4_zerobytes + array_frame_payload + array_frame_end
    

# Send a TCP/IP Frame to HRD with a command
def sendframe(commandstring):
    client.sendall(construct_frame(commandstring))
    return client.recv(4096).decode("utf-16")[8:-3]    

# Get the frequency from HRD and send it to APRS service
def get_frequency_and_send_APRS():
    frequency = sendframe("[" + str(radiostring[0:3]) + "] get frequencies")

    # Extract frequencies out of answer string
    frequency_vfo1 = frequency[0:frequency.index('-')]
    frequency_vfo2 = frequency[frequency.index('-')+1:]

    # Convert to MHz for readability
    string_vfo1 = '{:f}'.format(float(int(frequency_vfo1))/1000000.0) + " MHz"
    string_vfo2 = '{:f}'.format(float(int(frequency_vfo2))/1000000.0) + " MHz"

    
    print ("QRG VFO1:" + string_vfo1 + " QRG VFO2:" + string_vfo2)
    AIS.sendall(config.get('Main config', 'APRS_User') + ">APRS,TCPIP*,qAC,SEVENTH:qAC,T2ERFURT:!" + config.get('Position', 'Pos_N') + "/" + config.get('Position', 'Pos_E') + "- " + config.get('Main config', 'APRS_Desc'))
    AIS.sendall(config.get('Main config', 'APRS_User') + ">APRS,TCPIP*:>Currently QRV - QRG VFO1: " + string_vfo1 + " | QRG VFO2: " +  string_vfo2)
    
# init

# Check, if INI file exists. If not, create it and ask user for Callsign/PW
init_of_config()

# Connect to HRD IP Server
connect_to_HRD()

# Connect to APRS service
AIS = aprslib.IS(config.get('Main config', 'APRS_User'), passwd=config.get('Main config', 'APRS_PW'), port=14580)
AIS.connect()

radiostring = sendframe("get radios")
print ("Radio: " + radiostring)

# loop
while 1:
    
    get_frequency_and_send_APRS()
    
    time.sleep(60)
    



