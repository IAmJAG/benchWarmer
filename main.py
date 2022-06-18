from concurrent.futures import thread
import os
import sys
os.system('pyclean -q .')
os.system('cls')

from menu import initMenu, printMenu, MENU, assoc

# menuOptions = initMenu('menu.json')
# printMenu(menuOptions)

# sys.exit()

import scrcpy
import cv2 as cv

from helper import resizeCVImage
from adbutils import adb

devices = [i.serial for i in adb.device_list()]
device = None if len(devices)<=0 else devices[0]

adb.connect("192.168.18.13:4444")
client = scrcpy.Client(device=adb.device(serial=device), bitrate=1000000000)

def on_frame(frame):    
    if frame is not None:
        cv.imshow("viz", resizeCVImage(frame, height=800))
                   
    if cv.waitKey(10) == ord('q'):
        #Stop()
        client.stop()
        
def on_init():
    dvcs = [i.serial for i in adb.device_list()]
    devices.clear()
    for d in dvcs:
        devices.append(d)

client.add_listener(scrcpy.EVENT_FRAME, on_frame)
client.add_listener(scrcpy.EVENT_INIT, on_init)

menuOptions = []
mainMenu = initMenu('menu.json')

def initMainMenu(indx=None):
    menuOptions.clear()
    
    for mnu in mainMenu:
        menuOptions.append(mnu)
    
    MENU.clear()            
    assoc(0, menuOptions, Start)
    assoc(1, menuOptions, selectDevice)
    assoc(len(menuOptions)-1, menuOptions, quit)

def Stop(indx):
    client.stop()
        
def Start(indx):
    if client.alive: 
        print("Alive")
        client.stop()
        
    client.device = adb.device(serial=device)
    client.start(threaded=True)

def quit(indx):
    Stop(indx)
    os.system('pyclean -q .')
    sys.exit()    
    
def __selectDevice(indx):
    indx = int(indx)
    device = devices[indx]
    initMainMenu()

def selectDevice(indx):
    menuOptions.clear()
    for d in devices:
        dvc = {"Caption": d, "Keys": []}
        menuOptions.append(dvc)   
            
    MENU.clear()
    for i in range(len(menuOptions)):
        assoc(i, menuOptions, __selectDevice)
        
    menuOptions.append({"Caption": "[B]ack", "Keys": ["BACK", "B"]})
    assoc(len(menuOptions)-1, menuOptions, initMainMenu)   
    

initMainMenu()

while (True):    
    printMenu(menuOptions)
    try:        
        option = str(input("Please select an option: ")).upper()
    except:
        os.system('cls')
        print('Wrong input.Please select an option: ')            
    
    try:
        MENU[option](option)        
        os.system('cls')
    except KeyError:
        os.system('cls')
        print('Wrong input.Please select an option: ')    
    
