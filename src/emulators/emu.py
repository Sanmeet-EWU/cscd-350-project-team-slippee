from abc import ABC, abstractmethod

# Abstract parent class
class Emulator(ABC):
    inputFile = []

    # To be defined in child classes
    @abstractmethod
    def convert_file(self, inputFiles): # Might Remove this one
        pass

    @abstractmethod
    def split_file(file):
        pass

    # setter for inputFile
    def set_input_file(self, inFiles):
        inputFile = inFiles

    # def identify(inpStr): # Don't remember what this was for, putting it so I don't forget

    # Convert from little endian to big endian, and visa versa
    def endian_fix(self, inString):
        if not len(inString) % 4 == 0:
            print("Not Valid Save")
            exit(0)
        
        temp = b""
        for i in range(len(inString) // 4):
            temp += inString[i * 4: (i + 1) * 4][::-1]
        
        return temp

