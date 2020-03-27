from consts import START_ADDRESS
class CPU:
    def __init__(self):
        self.registers = [0] * 16  # general purpose registers (8 bits)
        self.index = 0  # index register  (16 bits)
        self.PC = START_ADDRESS  # program counter  (16 bits)
        self.SP = 0  # stack pointer  (8 bits)
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = [[0] * 32 for i in range(64)]
        self.opcode = 0
