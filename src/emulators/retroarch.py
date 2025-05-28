from .emu import Emulator
 

class RetroArch(Emulator):
    def convert_file(self, inputFile):
        print("Hi")


if __name__=="__main__":
    ret = RetroArch()
    ret.convert_file()
    print(ret.endian_fix(b"What"))
