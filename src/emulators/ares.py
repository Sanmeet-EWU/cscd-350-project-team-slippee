from emu import Emulator
from files import fileutils

class Ares(Emulator):
    def split_file(file):
        files = {}

        for f in file:
                temp = fileutils.readin(f)
                if f.endswith('eeprom') and len(temp) == 0x8000:
                    files['eeprom'] = temp
                elif f.endswith('eeprom') and len(temp) == 0x20000:
                    files['deeprom'] = temp
                elif f.endswith('flash'):
                    files['flash'] = temp
                elif f.endswith('pak'):
                    files['pak'] = temp
                elif f.endswith('ram'):
                    files['ram'] = temp
                else:
                    print("File Not Found")
        
        return files