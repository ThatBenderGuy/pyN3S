from collections import defaultdict

from instructions import StaAbsInstruction, LdaImmInstruction, SEIInstruction, CLDInstruction
from memory import RAM
from ppu import PPU
from rom import ROM
from status import Status

RAM_START_INCLUSIVE = int.from_bytes(bytes.fromhex('0000'), byteorder='big')
RAM_END_INCLUSIVE = int.from_bytes(bytes.fromhex('1FFF'), byteorder='big')

PPU_START_INCLUSIVE = int.from_bytes(bytes.fromhex('2000'), byteorder='big')
PPU_END_INCLUSIVE = int.from_bytes(bytes.fromhex('2007'), byteorder='big')

class CPU(object):
    def __init__(self, ram: RAM, ppu: PPU):
        self.ram = ram
        self.ppu = ppu
        # Status Registers: store a single byte
        self.status_reg = None  # type: Status

        # counter registers: store single byte
        self.pc_reg = None  # program counter
        self.sp_reg = None  # stack pointer

        # data registers: store a single byte
        self.x_reg = None  # x register
        self.y_reg = None  # y register
        self.a_reg = None  # a register

        # program counter stores current execution point
        self.running = True

        self.instructions = [
            SEIInstruction(),
            CLDInstruction(),
            LdaImmInstruction(),
            StaAbsInstruction()
        ]

        self.instructions_mapping = defaultdict()
        for instruction in self.instructions:
            self.instructions_mapping[instruction.identifier_byte] = instruction

        self.rom = None

    def start_up(self):
        """
        set the initial values of cpu registers 
        status reg: 000100 (IRQs disabled)
        x, y, a regs: 0
        stack pointer: $FD
        $4017: 0 (frame irq disabled)
        $4015: 0 (sound channels disabled)
        $4000-$400F: 0 (sound registers)
        """
        # TODO Hex vs Binary
        self.pc_reg = 0
        self.status_reg = Status()
        self.sp_reg = bytes.fromhex('FD')

        self.x_reg = 0
        self.y_reg = 0
        self.a_reg = 0

        # TODO Implement memory sets

    def get_memory_owner(self, location: int):
        """
        return the owner of a memory location
        """
        if RAM_START_INCLUSIVE <= location <= RAM_END_INCLUSIVE:
            return self.ram
        elif PPU_START_INCLUSIVE <= location <= PPU_END_INCLUSIVE:
            # pass off to the ppu register manager
            return self.ppu

    def run_rom(self, rom: ROM):
        # load rom
        self.rom = rom
        self.pc_reg = self.rom.header_size

        # run program
        self.running = True
        while self.running:
            # get the current byte at pc
            identifier_byte = self.rom.get_bytes(self.pc_reg)

            # turn the byte into an Instruction
            instruction = self.instructions_mapping.get(identifier_byte, None)
            if instruction is None:
                raise Exception('Instruction not found: {}'.format(identifier_byte))

            # get the correct amount of data bytes
            num_data_bytes = instruction.instruction_length - 1
            # get the data bytes
            data_bytes = self.rom.get_bytes(self.pc_reg + 1, num_data_bytes)

            # we have a valid instruction
            instruction.execute(self, data_bytes)

            self.pc_reg += instruction.instruction_length
