import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import test_bit
from anlageFunctions import setBitValue
from anlageFunctions import getPackage

ip = "192.168.200.236"
# init modbus client
c = ModbusClient(host=ip, port=502, unit_id=1,  auto_open=True)

beltSensorData = {
    """Register, Front, Back"""
    "A": [8002, 0, 1],
    "B": [8002, 2, 3],
    "D": [8002, 8, 9],
    "E": [8002, 10, 11],
    "G": [8001, 0, 1],
    "H": [8001, 2, 3],
    "I": [8001, 4, 5],
    "K": [8001, 10, 11],
    "L": [8004, 12, 13],
    "N": [8004, 2, 3],
    "O": [8004, 4, 5],
    "P": [8004, 6, 7],
    "T": [8003, 4, 5],
    "U": [8003, 6, 7],
    "V": [8003, 8, 9],
    "W": [8003, 10, 11],
    }

def getBeltSensorData(belt, pos):
    belt = belt.upper()
    pos = pos.upper()

    if pos == "F":  
        if test_bit(c, beltSensorData[belt][0], beltSensorData[belt][1]) == 1:
            return True
        else:
            return False
    elif pos == "B":
        if test_bit(c, beltSensorData[belt][0], beltSensorData[belt][2]) == 1:
            return True
        else:
            return False

beltData = {
    """Register, Forward, Backward"""
    "A": [8019, 0, 1],
    "B": [8019, 2, 3],
    "D": [8019, 8, 9],
    "E": [8019, 10, 11],
    "G": [8018, 0, 1],
    "H": [8018, 2, 3],
    "I": [8018, 4, 5],
    "K": [8018, 10, 11],
    "L": [8018, 12, 13],
    "N": [8021, 2, 3],
    "O": [8021, 4, 5],
    "P": [8021, 2, 3],
    "T": [8020, 4, 5],
    "U": [8020, 6, 7],
    "V": [8020, 8, 9],
    "W": [8020, 10, 11],
    }

def setBelt(belt, dir):    
    belt = belt.upper()
    dir = dir.upper()

    """dir: Forward = "F" , Backward = "B" , Stop = "S" """
    if (dir == "F"):
        setBitValue(True, c, beltData[belt][0], beltData[belt][1])
        setBitValue(False, c, beltData[belt][0], beltData[belt][2])
    elif (dir == "B"):
        setBitValue(False, c, beltData[belt][0], beltData[belt][1])
        setBitValue(True, c, beltData[belt][0], beltData[belt][2])
    elif (dir == "S"):
        setBitValue(False, c, beltData[belt][0], beltData[belt][1])
        setBitValue(False, c, beltData[belt][0], beltData[belt][2])


