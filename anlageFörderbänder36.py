import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import test_bit
from anlageFunctions import setBitValue
from anlageFunctions import getPackage

ip = "192.168.200.236"


# init modbus client
c = ModbusClient(host=ip, port=502, unit_id=1,  auto_open=True)
c.write_single_register(8018, 0)

while True:
    value = input("Decimal Wert: ")
    c.write_single_register(8018, int(value))
    print("Confirmed: ", bin(getPackage(c, 8018, 1)))

