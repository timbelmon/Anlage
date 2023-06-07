from pyModbusTCP.utils import set_bit
from pyModbusTCP.utils import reset_bit

def setBitValue(value, c, register, bit):
    regs_2 = c.read_holding_registers(register, 1)
    for write_reg in regs_2:
        if (value == True):
            write_reg = set_bit(write_reg, bit)
        elif (value == False):
            write_reg = reset_bit(write_reg, bit)
        c.write_single_register(register, write_reg)

def updatePackage(c, startRegister, amount):
    regs_l = c.read_holding_registers(startRegister, amount)
    for package in regs_l:
        return package