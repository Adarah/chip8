import pygame
from consts import START_ADDRESS
import random
from consts import SEED, pygame_keymap
import logging
from time import sleep, time

logging.basicConfig(
    filename="CPU.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class CPU:
    def __init__(self, memory, display_and_keyboard, keymapping):
        self.mem = memory
        self.dspkb = display_and_keyboard  # display and keyboard
        self.keymap = keymapping
        self.register = [0] * 16  # general purpose registers (8 bits)
        self.index = 0  # index register  (16 bits)
        self.PC = START_ADDRESS  # program counter  (16 bits)
        self.SP = 0  # stack pointer  (8 bits)
        self.delay_timer = 0
        self.sound_timer = 0
        self.opcode = 0
        self.pressed_keys = [0] * 16

        logging.debug(f"NEW EXECUTION {'-'*200}")

    # https://en.wikipedia.org/wiki/CHIP-8#Opcode_table
    def op_0NNN(self):
        # call to RCA 1802 program. Since we are not emulating that processor
        # I will leave this blank
        logging.critical("OP 0NNN called, this has not been implemented!")
        raise Exception(
            "Tried to execute operation that has not been implemented. Opcode = {}".format(
                format(self.opcode[0], "02X") + format(self.opcode[1], "02X")
            )
        )

    def op_00E0(self):
        """Clears the screen """
        # probably have to change the screen memory too
        logging.info("cleaning the screen")
        self.dspkb.video = [0] * 64 * 32
        self.dspkb.update()

    def op_00EE(self):
        """Return from subroutine"""
        logging.debug(f"stack pointer: {self.SP}")
        logging.debug(f"stack: {self.mem.stack}")
        logging.info("returning from subroutine")
        self.SP -= 1
        self.PC = self.mem.stack[self.SP]

    def op_1NNN(self):
        """Jump to addres NNN"""
        N = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        NNN = format(N, "X") + format(NN, "02X")  # converts to hex and concatenates
        self.PC = int(NNN, 16)
        logging.info(f"PC set to address {format(self.PC, '02X')}")

    def op_2NNN(self):
        """Call subroutine at NNN"""
        N = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        NNN = format(N, "X") + format(NN, "02X")  # converts to hex and concatenates
        logging.info(f"calling subroutine at {NNN}")
        self.mem.stack[self.SP] = self.PC
        logging.debug(f"stored PC in stack position {self.SP}")
        self.SP += 1
        self.PC = int(NNN, 16)
        logging.debug(f"stack: {self.mem.stack}")

    def op_3XNN(self):
        """Skip next instruction if VX equals NN"""
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        logging.info(f"skipping next instruction if V{X} == {NN}")
        if self.register[X] == NN:
            logging.debug("skipped!")
            self.PC += 2

    def op_4XNN(self):
        """Skips next instruction if Vx does not equal NN"""
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        logging.info(f"skipping next instruction if V{X} != {NN}")
        if self.register[X] != NN:
            logging.debug("skipped!")
            self.PC += 2

    def op_5XY0(self):
        """Skips next instruction if VX equals VY"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        logging.info(f"skipping next instruction if V{X} == V{Y}")
        if self.register[X] == self.register[Y]:
            logging.debug("skipped!")
            self.PC += 2

    def op_6XNN(self):
        """Sets VX to NN"""
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        logging.info(f"setting V{X} to {NN}")
        self.register[X] = NN

    def op_7XNN(self):
        """Adds NN to VX. Does not set the VF flag even if a carry happens"""
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        logging.info(f"V{X} = V{X} + {NN}")
        self.register[X] = (self.register[X] + NN) & 0xFF

    def op_8XY0(self):
        """Sets VX to the value of VY"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        logging.info(f"V{X} receives V{Y}")
        self.register[X] = self.register[Y]

    def op_8XY1(self):
        """Sets VX to the value of VX or VY (bitwise)"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        logging.info(f"V{X} = V{X} | V{Y}")
        logging.debug(f"V{X} = {bin(self.register[X])}")
        logging.debug(f"V{Y} = {bin(self.register[Y])}")
        self.register[X] |= self.register[Y]

    def op_8XY2(self):
        """Sets VX to the value of VX and VY (bitwise)"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        logging.info(f"V{X} = V{X} & V{Y}")
        logging.debug(f"V{X} = {bin(self.register[X])}")
        logging.debug(f"V{Y} = {bin(self.register[Y])}")
        self.register[X] &= self.register[Y]

    def op_8XY3(self):
        """Sets VX to the value of VX xor VY (bitwse)"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        logging.info(f"V{X} = V{X} ^ V{Y}")
        logging.debug(f"V{X} = {bin(self.register[X])}")
        logging.debug(f"V{Y} = {bin(self.register[Y])}")
        self.register[X] ^= self.register[Y]

    def op_8XY4(self):
        """VX += VY"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        addition = self.register[X] + self.register[Y]
        logging.info(f"V{X} += V{Y}")
        if addition > 255:
            self.register[-1] = 1
        else:
            self.register[-1] = 0
        self.register[X] = (addition) & 0xFF  # unsigned sum

    def op_8XY5(self):
        """VX -= VY"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        logging.info(f"V{X} -= V{Y}")
        if self.register[X] >= self.register[Y]:
            self.register[-1] = 1
        else:
            self.register[-1] = 0
        self.register[X] = (
            self.register[X] - self.register[Y]
        ) & 0xFF  # unsgined subtraction

    def op_8XY6(self):
        """Stores the least significant bit of VX in VF then right shifts
        VX by 1 (VX >> 1)"""
        X = self.opcode[0] & 0x0F
        self.register[-1] = self.register[X] & 0x01  # VF is the last register
        logging.debug(f"stores least significant bit in VF, then shits V{X} >> 1")
        logging.debug(f"V{X} = {bin(self.register[X])}")
        logging.debug(f"V{X} >> 1 = {bin((self.register[X] >> 1) & 0xFF)}")
        self.register[X] = (self.register[X] >> 1) & 0xFF

    def op_8XY7(self):
        """VX = VY - VX"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        if self.register[Y] >= self.register[X]:
            self.register[-1] = 1
        else:
            self.register[-1] = 0
        logging.debug(f"V{X} = V{Y} - V{X}")
        self.register[X] = (self.register[Y] - self.register[X]) & 0xFF

    def op_8XYE(self):
        """Stores the most significant bit of VX in VF and then left shifts
        VX by 1 (VX << 1)"""
        X = self.opcode[0] & 0x0F
        self.register[-1] = (self.register[X] & 0x80) >> 7  # VF is the last register
        logging.info(f"stores most significant bit in VF, then left shits V{X} << 1")
        logging.debug(f"V{X} = {bin(self.register[X])}")
        logging.debug(f"V{X} << 1 = {bin((self.register[X] << 1) & 0xFF)}")
        self.register[X] = (self.register[X] << 1) & 0xFF

    def op_9XY0(self):
        """skip next instruction if VX does not equal VY"""
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        logging.info(f"skip next instruction if V{X} != V{Y}")
        if self.register[X] != self.register[Y]:
            logging.debug("skipped!")
            self.PC += 2

    def op_ANNN(self):
        """Sets the index_register to the address NNN"""
        N = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        NNN = format(N, "02X") + format(NN, "02X")  # converts to hex and concatenates
        self.index = int(NNN, 16)
        logging.info(f"setting index register to {format(self.index, '02x')}")

    def op_BNNN(self):
        """Jumps to the address NNN plus V0"""
        N = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        NNN = format(N, "X") + format(NN, "02X")  # converts to hex and concatenates
        logging.info(f"setting PC to address {NNN} + V0 ({self.register[0]})")
        self.PC = int(NNN, 16) + self.register[0]

    def op_CXNN(self):
        """Sets VX to the bitwise and of a random number between 0 and 255 and NN"""
        X = self.opcode[0] & 0x0F
        NN = self.opcode[1]
        random_num = random.randint(0, 255)
        logging.info(f"setting V{X} to V{X} & random number {random_num}")
        logging.debug(f"V{X} = {bin(self.register[X])}")
        logging.debug(f"random_num = {bin(int(random_num))}")
        self.register[X] = random_num & NN

    def op_DXYN(self):
        # draws a sprite at coordinates (VX, VY) that has a width of 8 pixels and a height of N pixels.
        # Each row of 8 pixels is read as bit-coded starting from memory location I
        # I value doesn’t change after the execution of this instruction.
        # As described above, VF is set to 1 if any screen pixels are flipped
        # from set to unset when the sprite is drawn, and to 0 if that doesn’t happen
        # in other words, VF = 1 if collisions happened
        self.register[-1] = 0
        X = self.opcode[0] & 0x0F
        Y = (self.opcode[1] & 0xF0) >> 4
        N = self.opcode[1] & 0x0F  # height
        x_reg = self.register[X]
        y_reg = self.register[Y]
        logging.info(f"drawing at position {x_reg}, {y_reg}")
        logging.debug(f"index is at {format(self.index, '02X')}")
        logging.debug(f"index: {self.mem.memory[self.index: self.index+N]}")
        for height in range(0, N):
            sprite_line = self.mem.memory[self.index + height]
            for width in range(8):
                x_coord = (x_reg + width) % 64
                y_coord = (y_reg + height) % 32
                screen_pixel = self.dspkb.video[(y_coord * 64 + x_coord)]
                mask = 1 << (7 - width)
                if sprite_line & mask:
                    if screen_pixel:  # collision happened
                        self.register[-1] = 1
                # XORing screen pixels with the bits in sprite_line. each bit in sprite_line is a sprite pixel
                self.dspkb.video[(y_coord * 64 + x_coord)] ^= (sprite_line & mask) >> (7 - width)
        self.dspkb.draw_pixels()

    def op_EX9E(self):
        # skips next instruction if key stored in VX is pressed
        X = self.opcode[0] & 0x0F
        key_to_be_checked = pygame_keymap[self.register[X]]
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[key_to_be_checked]:
            self.PC += 2

    def op_EXA1(self):
        X = self.opcode[0] & 0x0F
        key_to_be_checked = pygame_keymap[self.register[X]]
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if not keys[key_to_be_checked]:
            self.PC += 2

    def op_FX07(self):
        """Sets VX to the value of the delay timer"""
        X = self.opcode[0] & 0x0F
        logging.info("setting V{X} to the value of the delay timer {self.delay_timer}")
        self.register[X] = self.delay_timer

    def op_FX0A(self):
        # A key press is awaited, and then stored in VX.
        # (Blocking Operation. All instruction halted until next key event)
        X = self.opcode[0] & 0x0F
        key_pressed = False
        while not key_pressed:
            # event = pygame.event.wait()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.unicode in self.keymap.keys():
                    key = self.keymap[event.unicode]
                    key_pressed = True
                    break
        self.register[X] = key

    def op_FX15(self):
        """Sets delay timer to VX"""
        X = self.opcode[0] & 0x0F
        logging.info(f"setting delay timer to V{X} = {self.register[X]}")
        self.delay_timer = self.register[X]

    def op_FX18(self):
        """Sets sounds timer to VX"""
        X = self.opcode[0] & 0x0F
        logging.info("setting sound timer to V{X}")
        self.sound_timer = self.register[X]

    def op_FX1E(self):
        # adds VX to I. VF is set to 1 when there is a range overflow (I+VX > 0xFFF)
        # and to 0 when there isn't
        X = self.opcode[0] & 0x0F
        logging.info(f"I += V{X}")
        logging.debug(f"index = {self.index}")
        if self.index + self.register[X] > 65535:
            self.register[-1] = 1
        else:
            self.register[-1] = 0
        self.index = (self.register[X] + self.index) & 0xFFFF
        logging.debug(f"index = {self.index}")

    def op_FX29(self):
        # sets I to the location of the sprite for the character in VX. Characters
        # 0-F(hex) are represented by a 4x5 font
        X = self.opcode[0] & 0x0F
        logging.info(f"setting index to the position of the character in V{X}")
        value = self.register[X] & 0x0F
        self.index = 0x50 + value * 5
        logging.debug(f"index = {self.index}")

    def op_FX33(self):
        # stores the BCD representation of VX, with the most significant of three
        # digits at the address in I, the middle digit at I+1, least significant
        # digit at I + 2.
        X = self.opcode[0] & 0x0F
        logging.info(
            f"storing BCD representation of V{X} in memory address {self.index}"
        )
        logging.debug(f"V{X} = {self.register[X]}")
        for idx, i in enumerate(format(self.register[X], "0>3d")):
            self.mem.memory[self.index + idx] = int(i)
            logging.debug(f"storing {int(i)} in memory position {self.index+idx}")
        logging.debug(f"memory: {self.mem.memory[self.index:self.index+3]}")

    def op_FX55(self):
        # stores V0 to VX(incliding VX) in memoy starting at address I. The offset
        # from I is increased by 1 fo reach value written, but I itself is left unmodified
        X = self.opcode[0] & 0x0F
        logging.debug(f"index = {self.index}")
        logging.debug(f"X = {X}")
        logging.debug(f"registers: {self.register}")
        for i in range(X + 1):
            logging.info(f"storing V{i} in memory position {self.index+i}")
            self.mem.memory[self.index + i] = self.register[i]
        logging.debug(f"memory array: {self.mem.memory[self.index:self.index+X+1]}")

    def op_FX65(self):
        # fills VO to VX(including VX) with values from memory starting at address I
        # The offsite from I is increased by 1 for each value written, but I itself is left unmodified
        X = self.opcode[0] & 0x0F
        logging.info(f"filling V0 to V{X} with values from memory address {self.index}")
        for i in range(X + 1):
            logging.debug(
                f"filling V{i} with value from memory position {self.index+i}"
            )
            self.register[i] = self.mem.memory[self.index + i]
        logging.debug(f"memory array: {self.mem.memory[self.index:self.index+X+1]}")

    def cycle(self):
        # instructions are 2 bytes long
        self.opcode = self.mem.memory[self.PC : self.PC + 2]
        for i in self.opcode:
            h = format(i, "02X")
            logging.debug(f"opcode: {h}")
        self.PC += 2
        logging.debug(f"PC: {hex(self.PC)}")
        self.decode_and_execute()
        logging.debug(f"registers: {self.register}")

    def decode_and_execute(self):
        def resolve_last_nibble(nibble):
            logging.debug(f"last nibble: {nibble}")
            last_nibble_ops = {
                0x00: self.op_8XY0,
                0x01: self.op_8XY1,
                0x02: self.op_8XY2,
                0x03: self.op_8XY3,
                0x04: self.op_8XY4,
                0x05: self.op_8XY5,
                0x06: self.op_8XY6,
                0x07: self.op_8XY7,
                0x0E: self.op_8XYE,
            }
            return last_nibble_ops[nibble]

        def resolve_last_byte(byte):
            logging.debug(f"last byte: {byte}")
            last_byte_ops = {
                0xA1: self.op_EXA1,
                0x9E: self.op_EX9E,
                0x07: self.op_FX07,
                0x0A: self.op_FX0A,
                0x15: self.op_FX15,
                0x18: self.op_FX18,
                0x1E: self.op_FX1E,
                0x29: self.op_FX29,
                0x33: self.op_FX33,
                0x55: self.op_FX55,
                0x65: self.op_FX65,
            }
            return last_byte_ops[byte]

        def resolve_zero(byte):
            logging.debug(f"zero_byte: {byte}")
            zero_ops = {0xE0: self.op_00E0, 0xEE: self.op_00EE}
            try:
                return zero_ops[byte]
            except Exception:
                return self.op_0NNN

        first_nibble = (self.opcode[0] & 0xF0) >> 4
        last_nibble = self.opcode[1] & 0x0F
        last_byte = self.opcode[1]
        logging.debug(f"first_nibble: {first_nibble}")
        operations = {
            0x0: resolve_zero,
            0x01: self.op_1NNN,
            0x02: self.op_2NNN,
            0x03: self.op_3XNN,
            0x04: self.op_4XNN,
            0x05: self.op_5XY0,
            0x06: self.op_6XNN,
            0x07: self.op_7XNN,
            0x08: resolve_last_nibble,
            0x09: self.op_9XY0,
            0x0A: self.op_ANNN,
            0x0B: self.op_BNNN,
            0x0C: self.op_CXNN,
            0x0D: self.op_DXYN,
            0x0E: resolve_last_byte,
            0x0F: resolve_last_byte,
        }
        if first_nibble == 0x08:
            operations[first_nibble](last_nibble)()
        elif first_nibble in [0x00, 0x0E, 0x0F]:
            operations[first_nibble](last_byte)()
        else:
            operations[first_nibble]()
