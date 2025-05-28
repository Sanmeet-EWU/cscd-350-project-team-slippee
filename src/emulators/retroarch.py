import os
import sys

# Get the absolute path of the 'src' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from emu import Emulator
 

class RetroArch(Emulator):
    def convert_file(self, inputFile):
        print("Hi")


if __name__=="__main__":
    ret = RetroArch()
    ret.convert_file()
    print(ret.endian_fix(b"What"))
