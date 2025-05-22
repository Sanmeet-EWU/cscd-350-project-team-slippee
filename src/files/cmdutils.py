def cmd_main(argv):
    if len(argv) == 0:
        print_usage()
        return -1
    elif "-h" in argv or "--help" in argv or "-help" in argv or "--h" in argv:
        print_usage()
        return -1
    elif "-v" in argv or "--version" in argv:
        print(version())
        return -1
    

def print_usage():
    '''
    Prints the usage of the program
    '''
    print('''
Usage: python main.py [options]

Options:
  -h, --help, -help, --h       Show this help message and exit
  -v, --version                Show the version of the program
  -f <emulator>                Specify the input emulator
  -t <emulator>                Specify the output emulator
  -i <input_file>              Specify the input file(s)
  -o <output_file>             Specify the output file
  -r <rom_location>            Rom to extract name from

Notes:
    -r option not necesarily required, but BizHawk could switch out underscores for spaces
    If no -o is specified, the output file will be the same name as the input file
    
Required options:
    -f <emulator>               Specify the input emulator
    -t <emulator>               Specify the output emulator
    -i <input_file>             Specify the input file(s)

Supported emulators (valid options):
    - Ares - ares, are 
    - bizhawk - BizHawk, biz, EmuHawk
    - retroarch - retroarch, ret
    - More to be added in the future

Example:
    python main.py -f ares -t bizhawk -i 'Dr. Mario 64 (USA).eeprom' -o 'Dr. Mario 64 (USA).SaveRAM' -r 'Dr. Mario 64 (USA).z64'
''')

    
def version():
    """
    Returns the version of the current package.
    """
    return "0.1.0"