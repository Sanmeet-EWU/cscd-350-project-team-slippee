from .emu import Emulator
from src.files import fileutils

import os

cwd = os.getcwd()
if os.path.basename(cwd) == "src":
    base_dir = os.path.dirname(cwd)
else:
    base_dir = cwd

# Shared paths
output_dir = os.path.join(base_dir, "src", "output")
template_dir = os.path.join(base_dir, "src", "template")

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)


bize = 0x0 # BizHawk eeprom start byte
bizp = 0x800 # BizHawk pak start byte
bizd = 0x8800 # Dezaemon 3D start byte
bizf = 0x20800 # BizHawk flash start byte
bizr = 0x40800 # BizHawk ram start byte
bizend = 0x48800 # End of File

# BizHawk(EmuHawk) Offsets
# + ------------ + ------------ + -------------- + ---------------- + --------------------------------------------- +
# | Type of Data | Start Offset | End Offset     | Size             | Notes                                         |
# + ------------ + ------------ + -------------- + ---------------- + --------------------------------------------- +
# | eeprom       | 0x0          | 0x200 or 0x800 | 512 B or 2,048 B | 2 different sizes                             |
# | pak          | 0x800        | 0x8800         | 32,768 B         |                                               |
# | ram          | 0x8800       | 0x20800        | 98,304 B         | For one specific game: Dezaemon 3D            |
# | flash        | 0x20800      | 0x40800        | 131,072 B        | Notably different Endianness than ares .flash |
# | ram          | 0x40800      | 0x48800        | 32,768 B         | Notably different Endianness than ares .ram   |
# + ------------ + ------------ + -------------- + ---------------- + --------------------------------------------- +
class BizHawk(Emulator):
    '''
    This is a class for the BizHawk emulator
    It is a child class of the Emulator parent class

    It allows for extraction of data from the file type:
    - SaveRAM

    It allows for writing to the same file type
    '''
    def convert_file(self, inputFiles: dict) -> None:
        '''
        Takes in a dictionary of bytestreams and writes each to their respective file

        inputFiles
            dictionary of the file bytestreams

        The file that get written to are as follows:
        - {filename}.SaveRAM

        '''
        fileutils.clone_template(f"{self.outfile}.SaveRAM", False)
        counter = 0

        with open(f"{output_dir}/{self.outfile}.SaveRAM", "r+b") as out:
            if 'eeprom' in inputFiles.keys():
                out.seek(0)
                out.write(inputFiles['eeprom'])
                counter += 1

            if 'pak' in inputFiles.keys():
                out.seek(bizp)
                out.write(inputFiles['pak'])
                counter += 1

            if 'dram' in inputFiles.keys():
                out.seek(bizd)
                out.write(inputFiles['dram'])
                counter += 1

            if 'flash' in inputFiles.keys():
                out.seek(bizf)
                out.write(self.endian_fix(inputFiles['flash']))
                counter += 1

            if 'ram' in inputFiles.keys():
                out.seek(bizr)
                out.write(self.endian_fix(inputFiles['ram']))
                counter += 1

        if counter == 0:
            return False, counter
        return True, counter

    def split_file(self, file: list) -> dict:
        '''
        split_file takes in a file name as a String
        It then reads in the file, and splits it based on the above table

        file
            the file(s) to split

        it returns a dictionary containing each file bytestreams
        '''
        files = {}

        if not isinstance(file, list):
            return {}
        
        inpFile = fileutils.readin(file[0])
        self.set_outfile(file[0][file[0].rfind("/") + 1:file[0].rfind(".")]) # Remove the path and extension from the file name

        files['eeprom'] = inpFile[bize:bizp]
        files['pak'] = inpFile[bizp:bizd]
        files['dram'] = inpFile[bizd:bizf]
        files['flash'] = self.endian_fix(inpFile[bizf:bizr])
        files['ram'] = self.endian_fix(inpFile[bizr:bizend])

        if self.is_empty(files['eeprom'], "eeprom") == 1:
            files.pop('eeprom')
        elif self.is_empty(files['eeprom'], "eeprom") == -1:
            files['eeprom'] = inpFile[bize:0x200]
        if self.is_empty(files['pak'], "pak") == 1:
            files.pop('pak')
        if self.is_empty(files['dram'], "dram") == 1 or "Daezmon" not in file[0]: # Fix a problem with non empty sections
            files.pop('dram')
        if self.is_empty(self.endian_fix(files['flash']), "flash") == 1:
            files.pop('flash')
        if self.is_empty(self.endian_fix(files['ram']), "ram") == 1:
            files.pop('ram')

        return files
    
    def is_empty(self, string: bytes, type: str) -> int:
        '''
        Checks if the given string is empty

        string
            the string to check

        type
            the type of string to check
        '''
        with open(f"{template_dir}/temp", "rb") as inp:
            if type == "eeprom":
                inp.seek(0)
                temp = inp.read(0x800)
                if temp == string:
                    return 1
                elif temp[0x200:0x800] == string[0x200:0x800]:
                    return -1
            elif type == "pak":
                inp.seek(0x800)
                temp = inp.read(0x8000)
                if temp == string:
                    return 1
            elif type == "dram":
                inp.seek(0x8800)
                temp = inp.read(0x18000)
                if temp == string:
                    return 1
            elif type == "flash":
                inp.seek(0x20800)
                temp = inp.read(0x20000)
                if temp == string:
                    return 1
            elif type == "ram":
                inp.seek(0x40800)
                temp = inp.read(0x8000)
                if temp == string:
                    return 1
        return 0