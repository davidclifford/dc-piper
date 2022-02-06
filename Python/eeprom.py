from numpy import uint16, uint8

out_bin = open("eeprom.bin", "wb")

v = 1
d = 0
for addr in range(1 << 17):
    v = addr & 0xF
    if v < 8:
        value = 1 << v
    else:
        value = 1 << (15-v)
    out_bin.write(uint8(value))

out_bin.close()
