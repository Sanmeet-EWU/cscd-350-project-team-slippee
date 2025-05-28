import os
import sys

# Get the absolute path of the 'src' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from .emu import Emulator
from files import fileutils

# Ares Files
# + ------------ + -------------------- + ------------------------------------------- +
# | Type of Data | Size                 | Notes                                       |
# + ------------ + -------------------- + ------------------------------------------- +
# | eeprom       | 512 B, 2 KB or 96 KB | 3 Different Sizes, 96 KB for Dezaemon 3D    |
# | pak          | 32 KB                | controller pak saves                        |
# | flash        | 128 KB               |                                             |
# | ram          | 32 KB                |                                             |
# + ------------ + -------------------- + ------------------------------------------- +
class Ares(Emulator):
    '''
    This is a class for the ares emulator

    It is a child class of the Emulator parent class

    It allows for extraction of data from the file types:  
    - eeprom
        - 512 B
        - 2 KiB
        - 96 KiB
    - flash
        - 128 KiB
    - pak
        - 32 KiB
    - rom
        - 32 KiB

    It allows for writing to the same file types
    '''
    def convert_file(self, inputFiles: dict) -> list:
        '''
        Takes in a dictionary of bytestreams and writes each to their respective file

        Returns a list containing whether a file was written, and how many files were written

        inputFiles
            dictionary of the file bytestreams
        
        The files that get written to are as follows:
        - {filename}.eeprom  
            **Note**: size is 512B or 2KB  
            **Note**: a special eeprom exists for Dezaemon 3D with size 96 KB

        - {filename}.flash
            
        - {filename}.pak

        - {filename}.ram
        '''
        counter = 0
        # All three of these write to an eeprom file
        # 512 B
        if 'eeprom' in inputFiles.keys():
            fileutils.writeout(f"{self.outfile}.eeprom", inputFiles['eeprom'])
            counter += 1
        # 2 KB
        if 'leeprom' in inputFiles.keys():
            fileutils.writeout(f"{self.outfile}.eeprom", inputFiles['leeprom'])
            counter += 1
        # 96 KB
        if 'deeprom' in inputFiles.keys():
            fileutils.writeout(f"{self.outfile}.eeprom", inputFiles['deeprom'])
            counter += 1
        # Writes to a flash file
        if 'flash' in inputFiles.keys():
            fileutils.writeout(f"{self.outfile}.flash", inputFiles['flash'])
            counter += 1
        # Writes to a pak file
        if 'pak' in inputFiles.keys():
            fileutils.writeout(f"{self.outfile}.pak", inputFiles['pak'])
            counter += 1
        # Writes to a ram file
        if 'ram' in inputFiles.keys():
            fileutils.writeout(f"{self.outfile}.ram", inputFiles['ram'])
            counter += 1
        
        if counter > 0:
            return True, counter
        else:
            return False, counter
    

    def split_file(self, file: list) -> dict:
        '''
        Takes in a list of files and reads them into a dictionary

        file
            the list of file names to read in

        Returns a dictionary containing each file
        
        for eeprom which has three different sizes, they are separated  
        with a different key for each:
        - eeprom for 512 B file
        - leeprom for 2 KB file
        - deeprom for 96 KB file
        '''
        files = {}
        
        if len(file) == 0:
            return {"error": "No files provided","file": file}

        # Not Valid
        if not isinstance(file, list):
            return {"error": "Input is not a list", "file": file}
        
        for f in file:
            # Not Valid Check
            if not isinstance(f, str):
                return {"error": "File is not a string", "file": file}

        self.set_outfile(file[0][file[0].rfind("/") + 1 :file[0].rfind(".")])

        for f in file:
                temp = fileutils.readin(f)

                if len(temp) == 0:
                    files['error'] = "File type not recognized"
                    files['file'] = f
                    continue

                if f.endswith('eeprom') and len(temp) == 0x200: # 512 B eeprom
                    files['eeprom'] = temp

                elif f.endswith('eeprom') and len(temp) == 0x800: # 2 KB eeprom 
                    files['leeprom'] = temp

                elif f.endswith('eeprom') and len(temp) == 0x18000: # 96 KB eeprom
                    files['deeprom'] = temp

                elif f.endswith('flash'):
                    files['flash'] = temp
                
                elif f.endswith('pak'):
                    files['pak'] = temp
                
                elif f.endswith('ram'):
                    files['ram'] = temp
                
                else:
                    files['error'] = "File type not recognized"
                    files['file'] = file
        
        return files