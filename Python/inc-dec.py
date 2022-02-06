#
# David Clifford 11/07/2021
#
# Create a 27c322 image to increment/decrement a 16 bit address
#
# Address 0-15 input 16 bit number
#
# Address 16-17 function:
#
# 00 = 0x0000
# 01 = increment
# 10 = decrement
# 11 = pass-through
#
from numpy import uint16

out_bin = open("inc-dec.bin", "wb")

for fun in range(1 << 2):
    for addr in range(1 << 16):
        value = addr
        if fun == 0:
            value = 0
        if fun == 1:
            value = (addr + 1) & 0xffff
        if fun == 2:
            value = (addr - 1) & 0xffff
        out_bin.write(uint16(value))

out_bin.close()
