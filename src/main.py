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

    emu_from, emu_to, input_files, output_file, rom_location = parse_args(args) # Parse the command line arguments
    
    file_dict = emu_from.split_file(input_files) # Split the input files into their respective components
    if output_file:
        if rom_location: # If a rom location is specified, use it to set the output file name
            
            rom = rom_location[rom_location.rfind("/") + 1:] # Remove the path from the rom location
            rom = rom[rom.rfind(".") + 1:] # Remove the extension from the rom name

            emu_to.set_outfile(output_file[output_file.rfind("/") + 1:] + rom) # Append the rom name to the output file name

        else: # If no rom location is specified, just use the output file name specified
            emu_to.set_outfile(output_file[output_file.rfind("/") + 1: output_file.rfind(".")]) 
    
    elif rom_location: # If no output file is specified, but a rom location is specified, use the rom name as the output file name
        rom = rom_location[rom_location.rfind("/") + 1:]
        emu_to.set_outfile(rom[rom.rfind(".") + 1:])

    else: # If no output file or rom location is specified, use the input emulator's output file name
        emu_to.set_outfile(emu_from.get_outfile())   
    
    emu_to.convert_file(file_dict) # Convert the input files to the output emulator's format


def main_web(args: list):
    if args == -1:
        exit(-1)

    emu_from, emu_to, input_files, output_file, rom_location = parse_args(args)

    file_dict = emu_from.split_file(input_files)
    if output_file:
        if rom_location:
            rom = rom_location[rom_location.rfind("/") + 1:]
            rom = rom[rom.rfind(".") + 1:]
            emu_to.set_outfile(output_file[output_file.rfind("/") + 1:] + rom)
        else:
            emu_to.set_outfile(output_file[output_file.rfind("/") + 1: output_file.rfind(".")])
    elif rom_location:
        rom = rom_location[rom_location.rfind("/") + 1:]
        emu_to.set_outfile(rom[rom.rfind(".") + 1:])
    else:
        emu_to.set_outfile(emu_from.get_outfile())

    emu_to.convert_file(file_dict)


def parse_args(args: list) -> tuple:
    '''
    Parses the command line arguments and returns the emulator objects and input files

    args
        The command line arguments passed to the script

    Returns
        A tuple containing the input emulator, output emulator, list of input files, output file name, and rom location

    
    If any required argument is missing, the function will print an error message and exit the program.
    '''
    emu_from, emu_to, input_files, output_file, rom_location = None, None, [], None, None
    if "-f" in args: # Input Emulator
        from_emu_index = args.index("-f")
        if from_emu_index + 1 < len(args) and args[from_emu_index + 1][0] != "-":
            try:
                print("Input Emulator:", end=" ")
                emu_from = get_emulator(args[from_emu_index + 1])
            except ValueError as e:
                print(e)
                exit(-1)
        else:
            print(args, "No input emulator specified")
            exit(-1)
    else:
        print(args,"No input emulator specified")
        exit(-1)
    
    if "-t" in args: # Output Emulator
        to_emu_index = args.index("-t")
        if to_emu_index + 1 < len(args) and args[to_emu_index + 1][0] != "-":
            try:
                print("Output Emulator:", end=" ")
                emu_to = get_emulator(args[to_emu_index + 1])
            except ValueError as e:
                print(e)
                exit(-1)
        else:
            print("No output emulator specified")
            exit(-1)
    else:
        print("No output emulator specified")
        exit(-1)
    
    if "-i" in args: # Input files
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
    
    if "-o" in args: # Output file
        output_index = args.index("-o")
        if output_index + 1 < len(args) and args[output_index + 1][0] != "-":
            output_file = args[output_index + 1]
        else:
            print("No output file specified")
    
    if "-r" in args: # Rom location
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

    Returns
        An instance of the emulator class corresponding to the given name
    
    Raises
        ValueError: If the emulator name is not recognized
    '''
    if emulator_name.lower() in ["ares", "are"]: # Ares Emulator
        print("Ares")
        return ares.Ares()
    elif emulator_name.lower() in ["bizhawk", "biz", "emuhawk"]: # BizHawk Emulator
        print("BizHawk (EmuHawk)")
        return bizhawk.BizHawk()
    elif emulator_name.lower() in ["retroarch", "ret"]: # RetroArch Emulator
        print("RetroArch")
        return retroarch.RetroArch()
    ##################################### 
    # Add more emulators here as needed #
    # Should only need to modify this   #
    #####################################
    else: # If the emulator name is not recognized, raise an error
        raise ValueError(f"Unknown emulator: {emulator_name}")


if __name__ == "__main__":
    main()
