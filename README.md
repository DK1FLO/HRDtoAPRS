# HRDtoAPRS
A simple python script which bridges HRD and APRS with the VFO frequency

# Installation

## Installation of Phython
In order to use this script, you need python installed on your local machine.
Python can be downloaded here: https://www.python.org/downloads/

Important: 
- Add Python 3.x to PATH
- Customize installation: pip (Install PIP)

## Installation of APRSlib:
This script is based on the APRSlib (https://pypi.org/project/aprslib/)
Use the following command (for example in Windows Command Line, cmd):

pip install aprslib

## Download this script
To download this script, you can use "clone and download" (upper right corner) to download the latest ZIP.
Extract the content to a path of your choice.

## Link script to HRD
In HamRadioDeluxe, navigate to Tools -> IP Server. Check, that the server is running and ensure that "Start server when HRD starts" is selected. 
As next step, go to Tools -> Programs -> Program launcher -> Manager 
In the upper left corner, you can find a symbol with "New definition", a new window opens. Click on \[...] and navigate to the path  where you copied the script file. Select "Start_APRS_TX.bat" (the combobox must be switched from .exe to .bat).
Afterwards, you are ready to go

# First start

The HRDtoAPRS script asks you to input some basic data, like:
- Callsign
- Password for APRS
- Description (I use "Flo out of Gerolfing", where Flo is my name and Gerolfing my town)
- Position
