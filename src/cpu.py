from consts import START_ADDRESS
from memory import Memory
from display import Display
import random


class CPU:
    def __init__(self, memory, display):
        self.mem = memory
        self.display = display
        self.register = ["00"] * 16  # general purpose registers (8 bits)
        self.index = 0  # index register  (16 bits)
        self.PC = START_ADDRESS  # program counter  (16 bits)
        self.SP = 0  # stack pointer  (8 bits)
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = [[0] * 32 for i in range(64)]
        self.opcode = 0

    # https://en.wikipedia.org/wiki/CHIP-8#Opcode_table
    def op_0NNN(self):
        # call to RCA 1802 program. Since we are not emulating that processor
        # i will leave this blank
        pass

    def op_00E0(self):
        """ clears the screen """
        # probably have to change the screen memory too
        self.display.screen.fill((0, 0, 0))

    def op_00EE(self):
        # Return from subroutine
        pass

    def op_1NNN(self, num: hex):
        """jump to addres NNN"""
        N = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        NNN = format(N, "X") + format(NN, "X")  # converts to hex and concatenates
        self.PC = int(NNN, 16)

    def op_2NNN(self):
        # call subroutine at NNN
        pass

    def op_3XNN(self):
        # skip next instruction if VX equals NN
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        if self.register[X] == NN:
            self.PC += 2

    def op_4XNN(self):
        # skips next instruction if Vx does not equal NN
        # if self.register
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        if self.register[X] != NN:
            self.PC += 2

    def op_5XY0(self):
        # skips next instruction if VX equals VY
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        if self.register[X] == self.register[Y]:
            self.PC += 2

    def op_6XNN(self):
        # sets VX to NN
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        self.register[X] = NN

    def op_7XNN(self):
        # adds NN to VX
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        self.register[X] += NN

    def op_8XY0(self):
        # sets VX to the value of VY
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        self.register[X] = self.register[Y]

    def op_8XY1(self):
        # sets VX to the value of VX or VY (bitwise)
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        self.register[X] |= self.register[Y]

    def op_8XY2(self):
        # sets VX to the value of VX and VY(bitwise)
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        self.register[X] &= self.register[Y]

    def op_8XY3(self):
        # sets VX to the value of VX xor VY (bitwse)
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        self.register[X] ^= self.register[Y]

    def op_8XY4(self):
        # VX += VY
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        self.register[X] += self.register[Y]

    def op_8XY5(self):
        # VX -= VY
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        self.register[X] -= self.register[Y]

    def op_8XY6(self):
        # stores the least significant bit of VX in VF then right shifts VX by 1 (VX >> 1)
        X = self.opcode[0] & 0x0F
        self.register[-1] = self.register[X] & 0x01  # VF is the last register
        self.register[X] = self.register[X] >> 1

    def op_8XY7(self):
        # VX = VY - VX
        # VX -= VY
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        self.register[X] = self.register[Y] - self.register[X]

    def op_8XYE(self):
        # stores the most significant bit of VX in VF and then left shifts VX by 1 (VX << 1)
        X = self.opcode[0] & 0x0F
        self.register[-1] = self.register[X] & 0x80  # VF is the last register
        self.register[X] = self.register[X] << 1

    def op_9XY0(self):
        # skip next instruction if VX does not equal VY
        X = self.opcode[0] & 0x0F
        Y = self.opcode[1] & 0xF0
        if self.register[X] != self.register[Y]:
            self.PC += 2

    def op_ANNN(self):
        # sets the index_register to the address NNN
        N = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        NNN = format(N, "X") + format(NN, "X")  # converts to hex and concatenates
        self.index = int(NNN, 16)

    def op_BNNN(self):
        # jumps to the address NNN plus V0
        N = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        NNN = format(N, "X") + format(NN, "X")  # converts to hex and concatenates
        self.PC = NNN + self.register[0]

    def op_CXNN(self):
        # sets VX to the bitwise and of a random number between 0 and 255 and NN
        X = self.opcode[0] & 0x0F
        random_num = random.uniform(0, 255)
        self.register[X] &= random_num

    def op_DXYN(self):
        # draws a sprite at coordinates (VX, VY) that has a width of 8 pixels and a height of N pixels.
        # Each row of 8 pixels is read as bit-coded starting from memory location I
        # I value doesn’t change after the execution of this instruction.
        # As described above, VF is set to 1 if any screen pixels are flipped
        # from set to unset when the sprite is drawn, and to 0 if that doesn’t happen
        # in other words, VF = 1 if collisions happened
        pass

    def op_EX9E(self):
        # skips next instruction if key stored in VX is pressed
        pass

    def op_EXA1(self):
        # skips next instruction if key stred in VX is NOT pressed
        pass

    def op_FX07(self):
        # sets VX to the value of the delay timer
        X = self.opcode[0] & 0x0F
        self.register[X] = self.delay_timer

    def op_FX0A(self):
        # A key press is awaited, and then stored in VX.
        # (Blocking Operation. All instruction halted until next key event)
        pass

    def op_FX15(self):
        # sets delay timer to VX
        X = self.opcode[0] & 0x0F
        self.delay_timer = self.register[X]

    def op_FX18(self):
        # sets sounds timer to VX
        X = self.opcode[0] & 0x0F
        self.sound_timer = self.register[X]

    def op_FX1E(self):
        # adds VX to I. VF is set to 1 when there is a range overflow (I+VX > 0xFFF)
        # and to 0 when there isn't
        pass

    def op_FX29(self):
        # sets I to the location of the sprite for the character in VX. Characters
        # 0-F(hex) are represented by a 4x5 font
        pass

    def op_FX33(self):
        # stores the BCD representation of VX, with the most significant of three
        # digits at the address in I, the middle digit at I+1, least significant
        # digit at I + 2.
        pass

    def op_FX55(self):
        # stores V0 to VX(incliding VX) in memoy starting at address I. The offset
        # from I is increased by 1 fo reach value written, but I itself is left unmodified
        pass

    def op_FX65(self):
        # fills VO to VX(including VX) with values from memory starting at address I
        # The offsite from I is increased by 1 for each value written, but I itself is left unmodified
        pass

    def cycle(self):
        # joins both bytes to form the instruction
        self.opcode = self.memory[self.PC : self.PC + 2]
        self.PC += 2
        ## DECODE
        ## EXECUTE
