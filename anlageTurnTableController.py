import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import test_bit
from anlageFunctions import setBitValue
from anlageFunctions import getPackage

class AnlageController:
    def __init__(self, ip):
        self.ip = ip
        self.c = ModbusClient(host=self.ip, port=502, unit_id=1, auto_open=True)
        self.anlage_sensor_values = {
            0: [False, "Teil in Position 1"],
            1: [False, "Teil in Position 3 (Bohrer)"],
            2: [False, "Teil in Position 2 (Prüfer)"],
            3: [False, "Bohrer in oben"],
            4: [False, "Bohrer ist unten"],
            5: [False, "Drehteller ist in Position"],
            6: [False, "Prüfer ausgefahren (Teil okay)"]
        }
        
    def update_turn_table_sensor_values(self, start_register):
        package = getPackage(self.c, start_register, 1)
        for i in self.anlage_sensor_values:
            self.anlage_sensor_values[i][0] = test_bit(package, i)
            i += 1

    def dump_turn_table_sensor_values(self):
        for i in self.anlage_sensor_values:
            print(self.anlage_sensor_values[i])
            
    def dump_turn_table_status(self):
        for i in self.anlage_sensor_values:
            if self.anlage_sensor_values[i][0]:
                print(self.anlage_sensor_values[i][1])
                
    def ejector_a(self, mode):
        if mode == "on" or mode == "eject":
            setBitValue(True, self.c, 8003, 7)
            time.sleep(0.5)
        if mode == "off" or mode == "eject":
            setBitValue(False, self.c, 8003, 7)
            
    def ejector_b(self, mode):
        if mode == "on" or mode == "eject":
            setBitValue(True, self.c, 8003, 6)
            time.sleep(0.5)
        if mode == "off" or mode == "eject":
            setBitValue(False, self.c, 8003, 6)
            
    def turn_turn_table(self):
        setBitValue(True, self.c, 8003, 1)
        time.sleep(0.2)
        setBitValue(False, self.c, 8003, 1)
        time.sleep(1)
        
    def check_part(self):
        setBitValue(True, self.c, 8003, 5)
        time.sleep(0.2)
        self.update_turn_table_sensor_values(8001)
        setBitValue(False, self.c, 8003, 5)
        time.sleep(0.2)
        return self.anlage_sensor_values[6][0]
    
    def bore_part(self):
        setBitValue(True, self.c, 8003, 4)
        time.sleep(0.2)
        setBitValue(True, self.c, 8003, 0)
        setBitValue(True, self.c, 8003, 2)
        time.sleep(0.5)
        setBitValue(False, self.c, 8003, 2)
        setBitValue(True, self.c, 8003, 3)
        time.sleep(0.5)
        setBitValue(False, self.c, 8003, 3)
        setBitValue(False, self.c, 8003, 0)
        setBitValue(False, self.c, 8003, 4)
