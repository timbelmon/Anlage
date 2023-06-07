import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import test_bit
from pyModbusTCP.utils import set_bit
from pyModbusTCP.utils import reset_bit

ip = "192.168.200.232"


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

def updatePackage(startRegister, amount):
    regs_l = c.read_holding_registers(startRegister, amount)
    for package in regs_l:
        return package

def updateTurnTableSensorValues(startRegister):
    package = updatePackage(startRegister, 1)
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
        
def setValueTrue(register, bit):
    regs_2 = c.read_holding_registers(register, 1)
    for write_reg in regs_2:
        write_reg = set_bit(write_reg, bit)
        c.write_single_register(register, write_reg)
    
def setValueFalse(register, bit):
    regs_2 = c.read_holding_registers(register, 1)
    for write_reg in regs_2:
        write_reg = reset_bit(write_reg, bit)
        c.write_single_register(register, write_reg)
        
def ejectorA(mode): 
    if (mode == "on" or mode == "eject"):
        setValueTrue(8003, 7)
        time.sleep(0.5)
    if (mode == "off" or mode == "eject"):
        setValueFalse(8003, 7)
    
def ejectorB(mode):
    if (mode == "on" or mode == "eject"):
        setValueTrue(8003, 6)
        time.sleep(0.5)
    if (mode == "off" or mode == "eject"):
        setValueFalse(8003, 6)
        
def turnTurnTable():
    setValueTrue(8003, 1)
    time.sleep(0.2)
    setValueFalse(8003, 1)
    time.sleep(1) 
    
def checkPart():
    setValueTrue(8003, 5)
    time.sleep(0.2)
    updateTurnTableSensorValues(8001)
    setValueFalse(8003, 5)
    time.sleep(0.2)
    if turnTableSensorValues[6][0] == True:
        return True
    else:
        return False
    
def borePart():
    setValueTrue(8003, 4)
    time.sleep(0.2)
    setValueTrue(8003, 0)
    setValueTrue(8003, 2)
    time.sleep(0.5)
    setValueFalse(8003, 2)
    setValueTrue(8003, 3)
    time.sleep(0.5)
    setValueFalse(8003, 3)
    setValueFalse(8003, 0)
    setValueFalse(8003, 4)
    

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

    
    
    
 
       