from ssl import ALERT_DESCRIPTION_UNSUPPORTED_CERTIFICATE
import sys
import json

# menuOption = [
#     { 
#         "Caption": "[L]ist Devices", 
#         "Keys": ["LISTDEVICES", "LD", "L"]
#     },    
#     {
#         "Caption": "[Q]uit", 
#         "Keys": ["QUIT", "Q"]
#     }
# ]

# with open("menu.json", 'w') as jfile:
#     json.dump(menuOption, jfile, indent=4)

# sys.exit()

MENU = {}

def initMenu(fName):
    with open(fName) as jfile:
        return json.load(jfile)    

def printMenu(mo=None):
    if mo == None:
        return 
    for mnu in range(len(mo)):
        cap = mo[mnu]["Caption"]
        print(f"{mnu}: {cap}")

def assoc(indx, mo, func):
    MENU[str(indx)] = func
    for s in mo[indx]["Keys"]:        
        MENU[s] = func
    
