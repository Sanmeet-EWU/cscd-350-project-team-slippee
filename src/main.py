import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))         
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

from emulators import emu
from emulators import ares
from emulators import bizhawk
from emulators import retroarch
from files import cmdutils
args = sys.argv[1:]

def main():
    out = cmdutils.cmd_main(args)
    if out == -1:
        exit(-1)

    emu_from, emu_to, input_files, output_file, rom_location = parse_args(args)
    
    file_dict = emu_from.split_files(input_files)
    if output_file:
        if rom_location:
            rom = rom_location[rom_location.rfind("/") + 1:]
            rom = rom[rom.rfind(".") + 1:]
        else:
            emu_to.set_outfile(output_file[output_file.rfind("/") + 1:] + rom) 
    elif rom_location:
        rom = rom_location[rom_location.rfind("/") + 1:]
        emu_to.set_outfile(rom[rom.rfind(".") + 1:])
    
    emu_to.convert_file(file_dict)
    
    

def parse_args(args: list) -> tuple:
    '''
    Parses the command line arguments and returns the emulator objects and input files
    '''
    if "-f" in args:
        from_emu_index = args.index("-f")
        if from_emu_index + 1 < len(args) and args[from_emu_index + 1][0] != "-":
            try:
                print("Input Emulator:", end=" ")
                emu_from = get_emulator(args[from_emu_index + 1])
            except ValueError as e:
                print(e)
                exit(-1)
        else:
            print("No emulator specified")
            exit(-1)
    else:
        print("No input emulator specified")
        exit(-1)

    if "-t" in args:
        to_emu_index = args.index("-t")
        if to_emu_index + 1 < len(args) and args[to_emu_index + 1][0] != "-":
            try:
                print("Output Emulator:", end=" ")
                emu_to = get_emulator(args[to_emu_index + 1])
            except ValueError as e:
                print(e)
                exit(-1)
        else:
            print("No emulator specified")
            exit(-1)
    
    if "-i" in args:
        in_index = args.index("-i")
        if in_index + 1 < len(args) and args[in_index + 1][0] != "-":
            input_files = args[in_index + 1:]
            for i in range(len(input_files)):
                if input_files[i][0] == "-":
                    input_files = input_files[:i]
                    break
        else:
            print("No input file specified")
            exit(-1)
    else:
        print("No input file specified")
        exit(-1)
    
    if "-o" in args:
        output_index = args.index("-o")
        if output_index + 1 < len(args) and args[output_index + 1][0] != "-":
            output_file = args[output_index + 1]
        else:
            print("No output file specified")
    
    if "-r" in args:
        rom_index = args.index("-r")
        if rom_index + 1 < len(args) and args[rom_index + 1][0] != "-":
            rom_location = args[rom_index + 1]
            if not os.path.exists(rom_location):
                print("Rom location does not exist")
        else:
            print("No rom location specified")
    
    return emu_from, emu_to, input_files, output_file, rom_location


def get_emulator(emulator_name: str) -> emu.Emulator:
    '''
    Returns the emulator object based on the given name

    emulator_name
        The name of the emulator to get
    '''
    if emulator_name.lower() in ["ares", "are"]:
        print("Ares")
        return ares.Ares()
    elif emulator_name.lower() in ["bizhawk", "biz", "emuhawk"]:
        print("BizHawk (EmuHawk)")
        return bizhawk.BizHawk()
    elif emulator_name.lower() in ["retroarch", "ret"]:
        print("RetroArch")
        return retroarch.RetroArch()
    else:
        raise ValueError(f"Unknown emulator: {emulator_name}")


if __name__ == "__main__":
    main()
