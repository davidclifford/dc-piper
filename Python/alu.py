# David Clifford 28/11/2021
#
# Create an ALU using the following operations
#
# A = LHS (8-BITS)
# B = RHS (8-BITS)
#
# OP = 5-BITS
# ----------------
# 8+8+5 = 21 BITS
#
# Ops
# -----
# 00 0
# 01 B-A
# 02 A+B
# 03 A+B+1
# 04 A-B
# 05 A-B-1
# 06 A*B
# 07 A**B
# 08 A/B
# 09 A%B
# 0a A&B
# 0b A|B
# 0c A^B
# 0d ASR A
# 0e AB DIV 10
# 0f AB MOD 10
# 10 A
# 11 A+1
# 12 B
# 13 B+1
# 14 -A
# 15 A-1
# 16 -B
# 17 B-1
# 18 !A
# 19 !B
# 1a LSL A
# 1b LSR A
# 1d ROL A
# 1e ROR A
# 1f LOG A (LOG2 A e.g. 128=7 64=6 32=5 16=4 8=3 4=2 2=1 1=0 0=0 etc)
# 1f EXP A (2^(A%8) 0=1 1=2 2=4 3=8 4=16 5=32 6=64 7=128)
#
# FLAGS  Carry Neg oVerflow Zero Gt Lt Hi Lo

from numpy import uint8, uint16

EXP = [1, 2, 4, 8, 16, 32, 64, 128]
OPS = ['0', 'B-A', 'A+B', 'A+B+1', 'A-B', 'A-B-1', 'A*B', 'A**B', 'A/B', 'A%B',
       'A&B', 'A|B', 'A^B', 'ASR A', 'DIV10', 'MOD10', 'A', 'A+1', 'B', 'B+1',
       '-A', 'A-1', '-B', 'B-1', '!A', '!B', 'LSL A', 'LSR A', 'ROL A',
       'ROR A', 'LOG A', 'EXP A']
alu_rom_file = open('alu.bin', 'wb')
flags = 0
carry = 0

CARRY = 1 << 0
OVER = 1 << 1
ZERO = 1 << 2
NEG = 1 << 3

for op in range(32):
    for a in range(256):
        for b in range(256):
            flags = 0
            carry = 0
            overflow = 0
            if op == 0:
                d = 0
            if op == 1:  # B-A
                na = (a ^ 0xff) + 1
                s = (b + na)
                d = s & 0xff
                carry = (s >> 8) & 1
                if (na < 0x80 and b < 0x80 and d >= 0x80) or (na >= 0x80 and b >= 0x80 and d < 0x80):
                    overflow = OVER
            if op == 2:  # A+B
                s = (a + b)
                d = s & 0xff
                carry = (s >> 8) & 1
                if (a < 0x80 and b < 0x80 and d >= 0x80) or (a >= 0x80 and b >= 0x80 and d < 0x80):
                    overflow = OVER
            if op == 3:  # A+B+1
                s = (a + b + 1)
                d = s & 0xff
                carry = (s >> 8) & 1
                if (a < 0x80 and b < 0x80 and d >= 0x80) or (a >= 0x80 and b >= 0x80 and d < 0x80):
                    overflow = OVER
            if op == 4:  # A-B
                nb = (b ^ 0xff) + 1
                s = (a + nb)
                d = s & 0xff
                carry = (s >> 8) & 1
                if (a < 0x80 and nb < 0x80 and d >= 0x80) or (a >= 0x80 and nb >= 0x80 and d < 0x80):
                    overflow = OVER
            if op == 5:  # A-B-1
                nb = (b ^ 0xff) + 1
                s = (a + nb)
                d = s & 0xff
                carry = (s >> 8) & 1
                if (a < 0x80 and nb < 0x80 and d >= 0x80) or (a >= 0x80 and nb >= 0x80 and d < 0x80):
                    overflow = OVER
            if op == 6:  # a*b low
                d = (a * b) & 0xff
            if op == 7:  # a*b high
                d = ((a * b) >> 8) & 0xff
            if op == 8:  # a/b
                d = 0
                if b > 0:
                    d = int(a / b)
                else:
                    overflow = OVER
            if op == 9:  # a mod b
                d = 0
                if b > 0:
                    d = int(a % b)
                else:
                    overflow = OVER
            if op == 10:  # a and b
                d = int(a & b)
            if op == 11:  # a or b
                d = int(a | b)
            if op == 12:  # a xor b
                d = int(a ^ b)
            if op == 13:  # ASR A
                d = (a >> 1) & 0xff
                d |= (a & 0x80)  # preserve sign bit
                carry = a & 1
            if op == 14:  # ab / 10
                x = b % 10
                d = int((a + x*256) / 10) & 0xff
            if op == 15:  # ab % 10
                x = b % 10
                d = int((a + x*256) % 10) & 0xff

            if op == 16:
                d = a
            if op == 17:
                s = (a + 1)
                d = s & 0xff
                carry = (s >> 8) & 1
                if a < 0x80 and d >= 0x80:
                    overflow = OVER
            if op == 18:
                d = b
            if op == 19:
                s = (b + 1)
                d = s & 0xff
                carry = (s >> 8) & 1
                if a < 0x80 and d >= 0x80:
                    overflow = OVER
            if op == 20:  # -A
                d = (0-a) & 0xff
            if op == 21:  # A-1
                s = (a - 1)
                d = s & 0xff
                carry = (s >> 8) & 1
                if a >= 0x80 and d < 0x80:
                    overflow = OVER
            if op == 22:  # -B
                d = (0-b) & 0xff
            if op == 23:  # B-1
                s = (b - 1)
                d = s & 0xff
                carry = (s >> 8) & 1
                if b >= 0x80 and d < 0x80:
                    overflow = OVER
            if op == 24:  # !A
                d = (a ^ 0xff) & 0xff
            if op == 25:  # !B
                d = (b ^ 0xff) & 0xff
            if op == 26:  # LSL A
                s = (a << 1)
                d = s & 0xff
                carry = (s >> 8) & 1
            if op == 27:  # LSR A
                d = (a >> 1) & 0xff
                carry = a & 1
            if op == 28:  # ROL A
                d = ((a << 1) & 0xff) | ((a >> 7) & 1)
                carry = (a >> 7) & 1
            if op == 29:  # ROR A
                d = ((a >> 1) & 0xff) | ((a & 1) << 7)
                carry = (a & 1)
            if op == 30:  # LOG A
                d = 0
                if a == 0:
                    overflow = OVER
                else:
                    for log in range(8):
                        if a >= EXP[log]:
                            d = log
            if op == 31:  # EXP A
                d = EXP[a & 0x07] & 0xff

            # Set zero and negative flags
            if d == 0:
                flags |= ZERO
            if d & 0x80 == 0x80:
                flags |= NEG
            flags |= (carry * CARRY)
            flags |= overflow

            # Write to rom
            print(OPS[op], 'A:', a, 'B:', b, '=', d, 'fl', ('0000'+bin(flags).replace('0b', ''))[-4:])
            alu_rom_file.write(uint16(uint8(d) | uint8(flags) << 8))

alu_rom_file.close()
