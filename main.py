import argparse

from cpu import CPU
from instructions import LDAInstruction
from rom import ROM


def main():
    # Set up command line arguments parser
    parser = argparse.ArgumentParser(description='NES Emulator')
    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='The location to the rom file')
    args = parser.parse_args()

    # load rom
    with open(args.rom_path, 'rb') as file:
        rom_bytes = file.read()

    rom = ROM(rom_bytes)

    # create cpu
    cpu = CPU()
    cpu.run_rom(rom)


if __name__ == '__main__':
    main()
