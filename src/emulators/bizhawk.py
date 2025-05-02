from emu import Emulator
from files import fileutils

bize = 0x800 # BizHawk eeprom end byte
bizp = 0x8800 # BizHawk pak end byte
bizd = 0x20800 # Dezaemon 3D end byte
bizf = 0x40800 # BizHawk flash end byte
bizr = 0x48800 # BizHawk ram end byte

# BizHawk(EmuHawk) Offsets
# + ------------ + ------------ + -------------- + ---------------- + ------------------------------------------- +
# | Type of Data | Start Offset | End Offset     | Size             | Notes                                       |
# + ------------ + ------------ + -------------- + ---------------- + ------------------------------------------- +
# | eeprom       | 0x0          | 0x200 or 0x800 | 512 B or 2,048 B | 2 different sizes                           |
# | pak          | 0x800        | 0x8800         | 32,768 B         |                                             |
# | eeprom       | 0x8800       | 0x20800        | 98,304 B         | For one specific game: Dezaemon 3D          |
# | flash        | 0x20800      | 0x40800        | 131,072 B        |                                             |
# | ram          | 0x40800      | 0x48800        | 32,768 B         | Notably different Endianness than ares .ram |
# + ------------ + ------------ + -------------- + ---------------- + ------------------------------------------- +
class BizHawk(Emulator):
    def convert_file(self, inputFiles):
        print("Hi")

    def split_file(file):
        files = {}
        inpFile = fileutils.readin(file)

        files['eeprom'] = inpFile[:bize]
        files['pak'] = inpFile[bize:bizp]
        files['deeprom'] = inpFile[bizp:bizd]
        files['flash'] = inpFile[bizd:bizf]
        files['ram'] = inpFile[bizf:]

        return files
