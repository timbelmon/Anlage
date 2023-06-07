import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import test_bit
from pyModbusTCP.utils import set_bit
from pyModbusTCP.utils import reset_bit

ip = "192.168.200.23"


# init modbus client
c = ModbusClient(host=ip, port=502, unit_id=1,  auto_open=True)
