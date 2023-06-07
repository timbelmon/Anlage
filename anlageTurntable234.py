import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import test_bit
from anlageFunctions import setBitValue
from anlageFunctions import getPackage

ip = "192.168.200.234"


# init modbus client
c = ModbusClient(host=ip, port=502, unit_id=1,  auto_open=True)

"""
Actors
0 - Bohrer einschalten
1 - Drehteller drehen
2 - Bohrer herunterfahren 
3 - Borer hochfahren
4 - Werkstück festhalten
5 - Prüfer ausfahren
6 - Auswerfer B betätigen
7 - Auswerfer A betätigen
"""

turnTableSensorValues = {
0: [False, "Teil in Position 1"],
1: [False, "Teil in Position 3 (Bohrer)"],
2: [False, "Teil in Position 2 (Prüfer)"],
3: [False, "Bohrer in oben"],
4: [False, "Bohrer ist unten"],
5: [False, "Drehteller ist in Position"],
6: [False, "Prüfer ausgefahren (Teil okay)"]
}

def updateTurnTableSensorValues(startRegister):
    package = getPackage(c, startRegister, 1)
    for i in turnTableSensorValues:
        turnTableSensorValues[i][0] = test_bit(package, i)
        i+=1

def dumpturnTableSensorValues(): 
    i = 0
    while i < len(turnTableSensorValues):
        print(turnTableSensorValues[i])
        i+=1 
        
def dumpTurnTableStatus():   
    i = 0
    while i < len(turnTableSensorValues):
        if turnTableSensorValues[i][0] == True:
            print(turnTableSensorValues[i][1])
        i+=1 
        
def ejectorA(mode): 
    if (mode == "on" or mode == "eject"):
        setBitValue(True, c, 8003, 7)
        time.sleep(0.5)
    if (mode == "off" or mode == "eject"):
        setBitValue(False, c, 8003, 7)
    
def ejectorB(mode):
    if (mode == "on" or mode == "eject"):
        setBitValue(True, c, 8003, 6)
        time.sleep(0.5)
    if (mode == "off" or mode == "eject"):
        setBitValue(False, c, 8003, 6)
        
def turnTurnTable():
    setBitValue(True, c, 8003, 1)
    time.sleep(0.2)
    setBitValue(False, c, 8003, 1)
    time.sleep(1) 
    
def checkPart():
    setBitValue(True, c, 8003, 5)
    time.sleep(0.2)
    updateTurnTableSensorValues(8001)
    setBitValue(False, c, 8003, 5)
    time.sleep(0.2)
    if turnTableSensorValues[6][0] == True:
        return True
    else:
        return False
    
def borePart():
    setBitValue(True, c, 8003, 4)
    time.sleep(0.2)
    setBitValue(True, c, 8003, 0)
    setBitValue(True, c, 8003, 2)
    time.sleep(0.5)
    setBitValue(False, c, 8003, 2)
    setBitValue(True, c, 8003, 3)
    time.sleep(0.5)
    setBitValue(False, c, 8003, 3)
    setBitValue(False, c, 8003, 0)
    setBitValue(False, c, 8003, 4)
    

partChecked = False
ejectPart = False

while True:
    turn = False

    time.sleep(0.2)
    updateTurnTableSensorValues(8001)
    if turnTableSensorValues[0][0] == True: # position 1
        time.sleep(0.7) #TODO Rausnehmen, nur für Demozwecke.
        turn = True
    if turnTableSensorValues[1][0] == True: # position 3
        if partChecked == True:
            borePart()
        partChecked = False
        ejectPart = True
        turn = True
    if turnTableSensorValues[2][0] == True: # position 2
        turn = True
        if (checkPart() == True):
            partChecked = True
    if (turn == True):
        turnTurnTable()
        if ejectPart == True:
            ejectPart = False
            ejectorB("eject")

    
    
    
 
       