import argparse

from pyN3S.cpu import CPU


def main():
    # Set up command line arguments parser
    parser = argparse.ArgumentParser(description='NES Emulator')
    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='The location to the rom file')
    args = parser.parse_args()

    # TODO: validate rom path is correct
    print(args.rom_path)

    # load rom
    with open(args.rom_path, 'rb') as file:
        lines = file.read()

    # create cpu
    cpu = CPU()
    # TODO unhardcode
    num_prg_block = 2
    instructions = lines[16:16+16384*num_prg_block]

    for instruction in instructions:
        cpu.process_instruction(instruction)
        break

if __name__ == '__main__':
    main()
