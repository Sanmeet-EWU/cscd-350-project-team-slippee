Looking at N64 save types, there are a total of four normal save types. These are eeprom, pak, sram and flash.
All data on types of saves found here: http://micro-64.com/database/gamesave.shtml
**Note**: All sizes in Kbit are from the source above.

**eeprom**
Comes in two sizes, 512 B (4 Kbit) and 2 KiB (16 Kbit). Is a chip on the cartridge. 
**sram**
Comes in two sizes, 32 KiB (256 Kbit) and 96 KiB (768 Kbit). Is a chip on the cartridge. 96 KiB is for one game only, which is Dezaemon 3D.
**pak**
Comes in one size, 32 KiB (256 Kbit). Is a cartridge placed in the back of the controller.
**flash**
Comes in one size, 128 KiB (1 Mbit). Is a chip on the cartridge.

From my understanding this is how each emulator saves each of the aforementioned types:

**Ares**
Each is saved in their own separate file type (\* is the name of the rom):
eeprom - \*.eeprom
sram - \*.ram
pak - \*.pak
flash - \*.flash

For the next two, they are saved in one file, and offsets into the file will be listed.

**BizHawk**
File name: \*.SaveRAM
eeprom
Both are saved at offset 0x0 in the file. Each game can only have one or the other.

pak
Saved at offset 0x800 in the file.

sram
Saved in two different locations based on the size. 96 KiB gets saved at offset 0x8800 in the file, and 32 KiB gets saved at 0x40800 in the file.

flash
Saved at offset 0x20800 in the file.

**RetroArch**
File name: \*.srm
eeprom 
Both are saved at offset 0x0 in the file. Each game can only have one or the other.

pak
Saved at offset 0x800 in the file.

sram
Saved in two different locations as well. 96 KiB gets saved at offset 0x8800, and 32 KiB gets saved at 0x20800 in the file.

flash
Saved at offset 0x28800 in the file.


--------------------------------- Code Documentation ----------------------------------------------------------------
## fileutils.py
**readin(file: str) -> bytes**
readin() takes in the name of a file, and reads in the contents as a byte string.

**params**
file - is the name of the file to read in including the location.
**Returns**: the bytes contained in a file
**Error**: If the file does not exist, or some other error is thrown. An empty string is returned if an error is thrown.

------------------------------------------------------------------------------------------------------------------------
**writeout(name: str, file: bytes) -> None**

Writes the given bytes to the given file.

**params**
name - the name of the file to write to
file - the bytes to write to the file

------------------------------------------------------------------------------------------------------------------------
**clone_template(name: str, overwrite: bool) -> None**

Clones the template file to the given name. The template is just a 290 KiB empty file that can be written to. The goal is to keep the size of BizHawk and RetroArch save files.

**params**    
name - the name of the file to clone to
overwrite - whether to do template 1 or 2. 1 is for BizHawk and 2 is for RetroArch.

## cmdutils.py
**cmd_main(argv: List) -> int**
Parses the arguments, and tells main to stop if no arguments are provided, or if a help argument is provided.
    
**Returns**
-1 if usage is requested or if no arguments are provided
0 if arguments are valid and usage is not requested

------------------------------------------------------------------------------------------------------------------------
**print_usage(): -> None**
Prints the usage of the tool.

## main.py
**main() -> None**
The main function of the command line. It uses argv to take in the input emulator, output emulator, input files and other non-essential arguments.
Reads in the data from one save type, and converts it to the save type of the desired emulator.

------------------------------------------------------------------------------------------------------------------------
**main_web(args: list) -> None**
The main function of the web interface. It uses argv to take in the input emulator, output emulator, input files and other non-essential arguments.
Reads in the data from one save type, and converts it to the save type of the desired emulator.

------------------------------------------------------------------------------------------------------------------------
**parse_args(args: list) -> tuple**
Parses the command line arguments and returns the emulator objects and input files.

**params**
args - The command line arguments passed to the script

**Returns**
A tuple containing the input emulator, output emulator, list of input files, output file name, and rom location.

**Error**
If any required argument is missing, the function will print an error message and exit the program.

------------------------------------------------------------------------------------------------------------------------
**get_emulator(emulator_name: str) -> emu.Emulator**
Returns the emulator object based on the given name

**params**
emulatori\_name - The name of the emulator to get

**Returns**
An instance of the emulator class corresponding to the given name
    
**Error**
ValueError: If the emulator name is not recognized


## emu.py
**class Emulator(ABC)**
The parent class for all emulator subclasses. Contains all requried functions and variables for each emulator.

**class variables**
inputFile: list - A list of the files to read in.
outfile: str - The name of the file to write to.

------------------------------------------------------------------------------------------------------------------------
**convert_file(self, inputFiles: dict) -> bool)**
Abstract method to be defined in child classes. Converts files to the correct syntax for the emulator

**params**
inputFiles - A dictionary of all the save types

**Returns**
A boolean indicating whether the conversion was successful or not.

------------------------------------------------------------------------------------------------------------------------
**split_file(self, file: list) -> dict**
Abstract method to be defined in child classes. Splits each file in the given list based on defined parameters.

**params**
file - list of files to split

**Returns**
A dictionary containing each files bytestreams with name as key.

------------------------------------------------------------------------------------------------------------------------
**endian_fix(self, inString: bytes) -> bytes)**
Switches the endianess of the input bytestream

**params**
inString - The input byte string to invert the endianess of.

**Returns**
The byte string that has had it's endianess converted.
An empty byte string if the string length is not divisible by 4.
